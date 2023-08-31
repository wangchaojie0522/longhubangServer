'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-08-31 16:50:11
FilePath: \webserve\myApp\views.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.http import JsonResponse
import baostock as bs
import pandas as pd
import tushare as ts
from .models import GPList

# Create your views here.

res =  {
        "code": 0,
        "data": [],
        "msg": ""
}
#获取当前交易日最新的股票代码和简称
token='b3252a4869a96c045a5111ed9f879b44bfcd0f02f2f84f9fe6d487a5'
pro = ts.pro_api(token)
def get_code():
    codes = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,industry,list_date')
    return codes
def insert_sql(data):
    try:
        gupiao = GPList(
            tscode = data['ts_code'],
            name = data['name'],
            symbol = data['symbol'],
            industry = data['industry'],
            list_date = data['list_date'],
        )
        gupiao.save()
    except:
        pass
def gupiaoRL(request):
    if request.method == 'POST':
        res['code'] = 200
        res['msg'] = "数据库已更新!"
        data =  get_code()
        print(data)
        for index, item in data.iterrows():
            if item['symbol']:
                insert_sql(item)

        return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)
def gupiaoK(request):
    if request.method == 'POST':
        res['code'] = 200
        res['msg'] = "数据库已更新!"
        
        return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)