# -*-coding:utf-8-*-
import requests
from requests import exceptions
import datetime
import time
from account.pkg.local_database import AuthUser, AuthGroup, PointsPoints, PointConfig, VipList, database
from dateutil.relativedelta import relativedelta


query = AuthGroup.select().where(AuthGroup.group_id == 3)
for user in query:
    try:
        a = AuthUser.select().where(AuthUser.id == user.user_id).get()
        print(a.username)
    except AuthUser.DoesNotExist:
        print('用户不存在')
        AuthGroup.delete().where(AuthGroup.user_id == user.user_id).execute()
