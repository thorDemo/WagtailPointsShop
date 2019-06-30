from account.pkg.local_database import VipList

list = VipList.select().where(VipList.id>=1)
for line in list:
    print(line.user_name)
    v = VipList.update({
        VipList.user_name: str(line.user_name).strip(),
    }).where(VipList.id==line.id)
    v.execute()

