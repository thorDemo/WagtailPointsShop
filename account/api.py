# -*-coding:utf-8-*-
import requests
import datetime
from .pkg.local_database import AuthUser, AuthGroup, PointsPoints, PointConfig
from dateutil.relativedelta import relativedelta


def auto_flush_db():

    """
    定时读取流水API
    VIP 用户流水有效期为 1年
    非VIP 用户流水有效期为 6个月
    积分计算起始日期 没有1年 或者6个月

    :return:
    """
    data = {
        's': 'touzhulist',
        'username': '',
        'pageRecordCount': 10,
        'pageIndex': 0,
        'start_time': '',
        'end_time': _now_date(),
    }
    temp = 1
    while True:
        data['pageIndex'] = temp
        data['start_time'] = _start_date()
        temp = temp + 1
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data)
        except Exception as e:
            continue
        init_data = response.json()
        if len(init_data['res']) == 0:
            print('**************** All Data Flush Over ****************')
            break
        for line in init_data['res']:
            print(line)
            user_name = line['username']
            points = int(float(line['effbet']))
            try:
                auth_user = AuthUser.create(
                    username=user_name,
                    # 密码 Ptyw1q2w3e$R
                    password='pbkdf2_sha256$150000$O0pe7bsaDiJH$3loF1px9HvE2xNzbFEbMbhA+bwenpDCCzzvlyuMIRw4=',
                    first_name='',
                    last_name='',
                    email='',
                    is_superuser=0,
                    is_staff=0,
                    is_active=1,
                    date_joined=now_time
                )
                auth_user.save()
                auth_group = AuthGroup.create(
                    user_id=auth_user.id,
                    group_id=3
                )
                auth_group.save()
            except Exception:
                print('user already exist')
            # 积分计算公式
            try:
                PointsPoints.get(user_name=user_name)
            except PointsPoints.DoesNotExist:
                print('%s <<< %s >>> points does not exist' % (now_time, user_name))
                pp = PointsPoints.create(
                    user_name=user_name,
                    all_water=points,
                    month_water=_user_month_water(user_name),
                )
                pp.save()
                if len(init_data['res']) < 10:
                    print('**************** All Data Flush Over ****************')
                    break
                print('%s <<< %s >>> : user date create over' % (now_time, user_name))
                continue

            q = PointsPoints.update({
                PointsPoints.all_water: points,
                PointsPoints.month_water: _user_month_water(user_name)
            }).where(PointsPoints.user_name == user_name)
            q.execute()

            print('%s <<< %s >>> user date update success' % (now_time, user_name))
            if len(init_data['res']) < 10:
                print('**************** All Data Flush Over ****************')
                break


def _last_month():
    """
    计算一月前的时间
    :return: string
    """
    date_now = datetime.datetime.now()
    delta = relativedelta(months=-1)
    date_mon = (date_now + delta).strftime('%Y-%m-%d')
    return date_mon


def _start_date():
    """
    获取积分计算起始时间
    :return:
    """
    p = PointConfig.get(id=1)
    return p.auto_flush


def _now_date():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    return now


def _user_month_water(username):
    data = {
        's': 'touzhulist',
        'username': username,
        'start_time': _last_month(),
        'end_time': _now_date(),
    }
    response = requests.post('http://game.www201.net:1888/jieko/interface.php', data=data)
    all_data = response.json()
    print(all_data)
    try:
        bet = float(all_data['res'][0]['effbet'])
    except IndexError:
        return 0
    return int(bet)


if __name__ == '__main__':
    auto_flush_db()
    while True:
        auto_flush_time = datetime.datetime.now().strftime('%H:%M:%S')
        if auto_flush_time == '00:10:00':
            auto_flush_db()

