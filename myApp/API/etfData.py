'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-09-01 13:17:08
FilePath: \webserve\myApp\views.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.http import JsonResponse
import baostock as bs
import pandas as pd
import tushare as ts
from myApp.models import ETFList
from django.http import JsonResponse, QueryDict

# Create your views here.

res =  {
        "code": 0,
        "data": [],
        "volavg": 0,
        "minVal": 0,
        "maxVal": 0,
        "msg": ""
}
res2 =  {
        "code": 0,
        "data": [],
        "count": 0,
        "pageSize": 10,
        "pageNum": 1,
        "msg": ""
}
#获取当前交易日最新的股票代码和简称
token='b3252a4869a96c045a5111ed9f879b44bfcd0f02f2f84f9fe6d487a5'
pro = ts.pro_api(token)
def get_code():
    codes = pro.fund_basic(market='E',status='L')
    return codes
def insert_sql(data):
    try:
        etf = ETFList(
            tscode = data['ts_code'],
            name = data['name'],
            management = data['management'],
            fund_type = data['fund_type'],
            found_date = data['found_date'],
            list_date = data['list_date'],
            issue_date = data['issue_date'],
            issue_amount = data['issue_amount'],
            invest_type = data['invest_type'],
            type = data['type'],
            p_value = data['p_value'],
        )
        etf.save()
    except:
        pass
def etfRL(request):
    if request.method == 'POST':
        res['code'] = 200
        res['msg'] = "数据库已更新!"
        data =  get_code()
        print(data)
        for index, item in data.iterrows():
            if item['ts_code']:
                insert_sql(item)

        return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)
def etfKInfo(request):
    if request.method == 'GET':
        tscodeP = request.GET.get('tscode') or ""
        start_dateP = request.GET.get('start_date') or ""
        end_dateP = request.GET.get('end_date') or ""
        etf_list = []
        df = pro.fund_daily(ts_code=tscodeP, start_date=start_dateP, end_date=end_dateP)
        df.sort_values("trade_date",inplace=True)
        volavg = df['vol'].mean()
        minVal = df['high'].mean()
        maxVal = df['low'].mean()
        for index, item in df.iterrows():
            etf_list.append(
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
        print(etf_list)
        res['code'] = 200
        res['msg'] = "查询成功"
        res['volavg'] = volavg
        res['minVal'] = minVal
        res['maxVal'] = maxVal
        res['data'] = etf_list
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)


def etf(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        tscodeP = request.GET.get('tscode') or ""
        pageNumP = int(request.GET.get('pageNum')) or 1
        pageSizeP = int(request.GET.get('pageSize')) or 10
        etf_obj = ETFList.objects.filter(tscode__contains=tscodeP).order_by('tscode').values() 
        etf_list = []
        for data in etf_obj[(pageNumP -1) * pageSizeP: pageNumP*pageSizeP - 1]:
            etf_list.append(data)
        res2['code'] = 200
        res2['msg'] = "查询成功"
        res2['pageNum'] = pageNumP
        res2['pageSize'] = pageSizeP
        res2['count'] = len(etf_obj)
        res2['data'] = etf_list
        return JsonResponse(res2, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        id = request.GET.get('tscode')
        etf=ETFList.objects.filter(tscode=id)
        etf.delete()
        res['code'] = 200
        res['msg'] = "删除成功"
        return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)
