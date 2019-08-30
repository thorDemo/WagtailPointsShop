# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from orders.models import Orders
# from points.models import Points, Cost
from points.models import Points
from django.shortcuts import redirect
from mulu.models import GoodsPage, LimitBargainsPage
# from django.contrib import messages


@csrf_protect
def new_order(request):
    data = request.POST
    try:
        address = data['Address']
    except Exception:
        address = '虚拟商品不写地址'
    # 添加订单

    order = Orders(
        take_name=data['Name'],
        user_name=request.user.username,
        goods=data['Goods'],
        goods_id=data['GoodsID'],
        email=data['Email'],
        phone=data['Phone'],
        wechart=data['WeChart'],
        address=address,
        discount=data['Discount'],
        real_cost=data['Real'],
        image_id=int(data['Image']),
        tips=data['Tips'],
        cost=data['Cost'],
        status=0,
    )
    # # 积分 消费
    # cost = Cost(
    #     user_name=request.user.username,
    #     goods=data['Goods'],
    #     goods_id=data['GoodsID'],
    #     change_points=(int(data['Cost']) * -1),
    #     tips='礼品兑换',
    # )
    order.save()
    # cost.save()

    return redirect('/accounts/')
