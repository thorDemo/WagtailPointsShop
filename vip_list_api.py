from account.pkg.local_database import VipList, PointsPoints
from peewee import IntegerField

# list = VipList.select().where(VipList.id>=1)
# for line in list:
#     print(line.user_name)
#     v = VipList.update({
#         VipList.user_name: str(line.user_name).strip(),
#     }).where(VipList.id==line.id)
#     v.execute()

file = open('viplist/vip.txt', 'r', encoding='utf-8')
for line in file:
    line = line.strip()
    data = line.split(' ')
    VipList.insert({
        'user_id': data[0],
        'user_name': data[1],
        'user_level': data[2],
        'change_time': '2019-06-29'
    }).execute()
    try:
        if data[2] == '大客层':
            PointsPoints.insert({
                'user_name': data[0],
                'one_year_capital_flow': 0,
                'half_year_capital_flow': 0,
                'one_month_capital_flow': 0,
                'one_year_lottery': 0,
                'half_year_lottery': 0,
                'month_lottery': 0,
                'user_level': 6,
            }).execute()
        else:
            PointsPoints.insert({
                'user_name': data[0],
                'one_year_capital_flow': 0,
                'half_year_capital_flow': 0,
                'one_month_capital_flow': 0,
                'one_year_lottery': 0,
                'half_year_lottery': 0,
                'month_lottery': 0,
                'user_level': 5,
            }).execute()
    except IntegerField:
        print(data[0])