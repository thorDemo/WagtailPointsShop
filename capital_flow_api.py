# -*-coding:utf-8-*-
import requests
from requests import exceptions
import datetime
import time
from account.pkg.local_database import AuthUser, AuthGroup, PointsPoints, PointConfig, VipList, database
from dateutil.relativedelta import relativedelta


"""
    ** 设计需求 **
    1、定时读取流水API
    2、VIP 用户流水有效期为 1年
    3、非VIP 用户流水有效期为 6个月
    4、积分计算起始日期 没有1年 或者6个月
    5、多线程 提高速度
    6、异常处理
"""


# 刷新一个用户的流水信息
def flush_one_user(username, start_time, end_time):
    """
    'status': True, 'res': [{'username': 'wx5885', 'effbet': '201798780.00'}], 'PageCount': 1, 'PageIndex': 1}
    :param username:
    :param start_time:
    :param end_time:
    :return: Mix
    """
    data = {
        's': 'touzhulist',
        'username': username,
        'pageRecordCount': 10,
        'pageIndex': 0,
        'start_time': start_time,
        'end_time': end_time,
    }
    try:
        response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data)
        user_data = response.json()
        print(user_data)
        return user_data['res'][0]

    except Exception:
        # 请求异常
        print('网络异常 重试')
        time.sleep(2)

        flush_one_user(username, start_time, end_time)


# 刷新所有用户的信息
def flush_all_user():
    """
    :return:
    """
    page_index = 1    # 页码
    while True:
        try:
            data = {
                's': 'touzhulist',
                'username': '',
                'pageRecordCount': 100,
                'pageIndex': page_index,
                'start_time': _start_date(),
                'end_time': _now_date(),
            }
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data, timeout=2)
            if response.status_code == 403:
                print('%s nginx 403 等待10s 继续' % datetime.datetime.now())
                time.sleep(10)
                continue
        except exceptions.Timeout:
            print('%s 网络连接超时！ 3s 后重试' % datetime.datetime.now())
            continue
        init_data = response.json()
        if len(init_data['res']) == 0:
            print('**************** All Name Read Over ****************')
            break
        print('%s %s - %s 数据初始化' % (datetime.datetime.now(), (page_index-1) * 100, page_index*100))
        user_data = init_data['res']
        username_array = []
        for x in user_data:
            username_array.append(x['username'])

        one_year = one_year_capital_flow(page_index)
        while one_year is None:
            one_year = one_year_capital_flow(page_index)
        half_year = half_year_capital_flow(page_index)
        while half_year is None:
            half_year = half_year_capital_flow(page_index)
        one_month = one_month_capital_flow(page_index)
        while one_month is None:
            one_month = one_month_capital_flow(page_index)
        save_user_data(username_array, one_year, half_year, one_month)
        page_index += 1       # 页码加1

    print('**************** All Data Flush Over ****************')


# 保存用户数据
def save_user_data(username_array, one_year, half_year, one_month):
    data_temp = 0
    for username in username_array:
        # 如果用户存在
        print(username)
        try:
            user = AuthUser.select().where(AuthUser.username == username).get()
            print('%s %s 用户已经存在 更新数据' % (datetime.datetime.now(), user.username))
            a = AuthUser.update({
                AuthUser.first_name: '佚',
                AuthUser.last_name: '名',
                AuthUser.email: '%s@bmw1984.com' % username,
                AuthUser.is_superuser: 0,
                AuthUser.is_staff: 0,
                AuthUser.is_active: 1,
            }).where(AuthUser.username == username)
            p = PointsPoints.update({
                PointsPoints.one_year_capital_flow:  int(float(one_year[data_temp]['effbet'])),
                PointsPoints.half_year_capital_flow: int(float(half_year[data_temp]['effbet'])),
                PointsPoints.one_month_capital_flow: int(float(one_month[data_temp]['effbet'])),
            }).where(PointsPoints.user_name == username)
            a.execute()
            p.execute()
            user_group_set(username)
        except TypeError:
            print('no type 数据异常')
        except AuthUser.DoesNotExist:
            # 如果用户不存在
            print('%s %s 用户不存在 新建' % (datetime.datetime.now(), username))
            sql_user_data = {
                'username': username,
                'password': 'pbkdf2_sha256$150000$O0pe7bsaDiJH$3loF1px9HvE2xNzbFEbMbhA+bwenpDCCzzvlyuMIRw4=',
                'first_name': '佚',
                'last_name': '名',
                'email': '%s@bmw1984.com' % username,
                'is_superuser': 0,
                'is_staff': 0,
                'is_active': 1,
                'date_joined': '2019-06-01 08:14:51.856783',
            }
            sql_points_data = {
                'user_name': username,
                'one_year_capital_flow': int(float(one_year[data_temp]['effbet'])),
                'half_year_capital_flow': int(float(half_year[data_temp]['effbet'])),
                'one_month_capital_flow': int(float(one_month[data_temp]['effbet'])),
            }
            AuthUser.insert(sql_user_data).execute()
            PointsPoints.insert(sql_points_data).execute()
            # 时间BUG 处理
            database.execute_sql('update auth_user set date_joined = ? where username = ?', ('2019-06-10 08:14:51.856783', username))
            user_group_set(username)

        data_temp += 1


# 用户分组设置
def user_group_set(username):
    u = AuthUser.select().where(AuthUser.username == username).get()
    user_id = u.id
    try:
        g = AuthGroup.select().where(AuthGroup.user_id == user_id).get()
        a = AuthGroup.update({
            AuthGroup.user_id: user_id,
            AuthGroup.group_id: 3
        }).where(AuthGroup.user_id == g.user_id)
        a.execute()
    except AuthGroup.DoesNotExist:
        AuthGroup.insert({
            'user_id': user_id,
            'group_id': 3,
        }).execute()


# 用户积分信息更新
def one_year_capital_flow(page_index):
    """
    一年总流水
    :param page_index:
    :return:
    """
    if over_one_year():     #起始时间超过一年 多余时间积分过期
        data = {
            's': 'touzhulist',
            'username': '',
            'pageRecordCount': 100,
            'pageIndex': page_index,
            'start_time': _last_year(),
            'end_time': _now_date(),
        }
        # print(data)
        try:
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data, timeout=2)
            all_data = response.json()
            print(all_data)
            return all_data['res']
        except IndexError:
            return 0
        except exceptions.Timeout:
            print('%s网络连接超时！one_year_capital_flow 1秒后重试' % datetime.datetime.now())
            time.sleep(1)
            one_year_capital_flow(page_index)
    else:
        data = {
            's': 'touzhulist',
            'username': '',
            'pageRecordCount': 100,
            'pageIndex': page_index,
            'start_time': _start_date(),
            'end_time': _now_date(),
        }
        # print(data)
        try:
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data, timeout=2)
            all_data = response.json()
            return all_data['res']
        except IndexError:
            return 0
        except exceptions.Timeout:
            print('%s网络连接超时！ one_year_capital_flow 1秒后重试' % datetime.datetime.now())
            time.sleep(1)
            one_year_capital_flow(page_index)


# 用户积分信息更新
def half_year_capital_flow(page_index):
    """
    半年总流水
    :param page_index:
    :return:
    """
    if over_half_year():     #起始时间超过半年 多余时间积分过期
        data = {
            's': 'touzhulist',
            'username': '',
            'pageRecordCount': 100,
            'pageIndex': page_index,
            'start_time': _half_year(),
            'end_time': _now_date(),
        }
        # print(data)
        try:
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data, timeout=2)
            all_data = response.json()
            return all_data['res']
        except IndexError:
            return 0
        except exceptions.Timeout:
            print('%s网络连接超时！ half_year_capital_flow 1秒后重试' % datetime.datetime.now())
            time.sleep(1)
            half_year_capital_flow(page_index)
    else:
        data = {
            's': 'touzhulist',
            'username': '',
            'pageRecordCount': 100,
            'pageIndex': page_index,
            'start_time': _start_date(),
            'end_time': _now_date(),
        }
        # print(data)
        try:
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data, timeout=2)
            all_data = response.json()
            return all_data['res']
        except IndexError:
            return 0
        except exceptions.Timeout:
            print('%s网络连接超时！ half_year_capital_flow 1秒后重试' % datetime.datetime.now())
            time.sleep(1)
            half_year_capital_flow(page_index)


# 用户积分信息更新
def one_month_capital_flow(page_index):
    """
    一个月流水
    :param page_index:
    :return:
    """
    data = {
        's': 'touzhulist',
        'username': '',
        'pageRecordCount': 100,
        'pageIndex': page_index,
        'start_time': _last_month(),
        'end_time': _now_date(),
    }
    try:
        response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data, timeout=2)
        all_data = response.json()
        return all_data['res']
    except IndexError:
        print('%s数据异常！ one_month_capital_flow 1秒后重试' % datetime.datetime.now())
        time.sleep(1)
        return 0
    except exceptions.Timeout:
        print('%s网络连接超时！ one_month_capital_flow 1秒后重试' % datetime.datetime.now())
        time.sleep(1)
        return 0


# 判断当前时间是否超过起始时间半年
def over_half_year():
    date_now = datetime.datetime.now()
    delta = relativedelta(months=-6)
    start_date = datetime.datetime.strptime(_start_date(), '%Y-%m-%d')
    date_half = date_now + delta - start_date
    if '-' in str(date_half):
        return False
    return True


# 判断当前时间是否超过起始时间一年
def over_one_year():
    date_now = datetime.datetime.now()
    delta = relativedelta(years=-1)
    start_date = datetime.datetime.strptime(_start_date(), '%Y-%m-%d')
    date_half = date_now + delta - start_date
    if '-' in str(date_half):
        return False
    return True


def _last_month():
    """
    计算一月前的时间
    :return: string
    """
    date_now = datetime.datetime.now()
    delta = relativedelta(months=-1)
    date_mon = (date_now + delta).strftime('%Y-%m-%d')
    return date_mon


def _half_year():
    """
    计算6个月前的时间
    :return: string
    """
    date_now = datetime.datetime.now()
    delta = relativedelta(months=-6)
    date_mon = (date_now + delta).strftime('%Y-%m-%d')
    return date_mon


def _last_year():
    """
    计算年月前的时间
    :return: string
    """
    date_now = datetime.datetime.now()
    delta = relativedelta(years=-1)
    date_mon = (date_now + delta).strftime('%Y-%m-%d')
    return date_mon


def _start_date():
    """
    获取积分计算起始时间
    :return:
    """
    p = PointConfig.get(id=1)
    # return '2018-06-06'
    return p.auto_flush


def _now_date():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now


flush_all_user()
# print(one_month_capital_flow(2))
# print(flush_one_user('pxlliao', '2019-06-01', '2019-06-11'))
# print(flush_one_user('loveft2018', '2019-05-11', '2019-06-11'))

# users = AuthUser.select().where(AuthUser.username != 'Thor')
# for user in users:
#     email = '%s@bmw1984.com' % user.username
#     print(email)
#     a = AuthUser.update({
#         AuthUser.first_name: '佚',
#         AuthUser.last_name: '名',
#         AuthUser.email: email
#     }).where(AuthUser.username == user.username)
#     a.execute()


