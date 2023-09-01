'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-09-01 10:11:05
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
        "volavg": 0,
        "minVal": 0,
        "maxVal": 0,
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
def gupiaoKInfo(request):
    if request.method == 'GET':
        tscodeP = request.GET.get('tscode') or ""
        start_dateP = request.GET.get('start_date') or ""
        end_dateP = request.GET.get('end_date') or ""
        ktypeP = request.GET.get('ktype') or "d"
        gupiao_list = []
        if ktypeP == 'd':
            df = pro.daily(ts_code=tscodeP, start_date=start_dateP, end_date=end_dateP)
            df.sort_values("trade_date",inplace=True)
        elif ktypeP == 'w':
            df = pro.weekly(ts_code=tscodeP, start_date=start_dateP, end_date=end_dateP)
            df.sort_values("trade_date",inplace=True)
        elif ktypeP == 'm':
            df = pro.monthly(ts_code=tscodeP, start_date=start_dateP, end_date=end_dateP)
            df.sort_values("trade_date",inplace=True)
        else:
            df = pro.daily(ts_code=tscodeP, start_date=start_dateP, end_date=end_dateP)
            df.sort_values("trade_date",inplace=True)

        volavg = df['vol'].mean()
        minVal = df['high'].mean()
        maxVal = df['low'].mean()
        for index, item in df.iterrows():
            gupiao_list.append(
                {
                    'ts_code': item['ts_code'],
                    'trade_date':item['trade_date'],
                    'open':item['open'],
                    'high':item['high'],
                    'low':item['low'],
                    'close':item['close'],
                    'pre_close':item['pre_close'],
                    'change':item['change'],
                    'pct_chg':item['pct_chg'],
                    'vol':item['vol'],
                    'amount':item['amount'],
                }
            )
        print(gupiao_list)
        res['code'] = 200
        res['msg'] = "查询成功"
        res['volavg'] = volavg
        res['minVal'] = minVal
        res['maxVal'] = maxVal
        res['data'] = gupiao_list
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)