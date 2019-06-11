from pkg.local_database import VipList
from datetime import datetime

# VipList.create_table()

file = open('vip.txt', 'r', encoding='utf-8')
for line in file:
    print(line)
    now = datetime.now()
    v = VipList(user_name=line, change_time=datetime.now())
    v.save()
