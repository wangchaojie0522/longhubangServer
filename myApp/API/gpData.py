'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-09-01 12:41:22
FilePath: \webserve\myApp\views.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.http import JsonResponse
import baostock as bs
import pandas as pd
import tushare as ts
from myApp.models import GPList
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


def gupiao(request):
    if request.method == 'POST':
        pass
    # ##判断POST请求body是否为空
    # if request.body.decode() == '':
    #     res['code'] = 1
    #     res['msg'] = "参数不能为空!"
        
    #     return JsonResponse(res)
    # ##不为空就将body转换成字典
    # else:
    #     body = eval(request.body)
    # ##确保字段不为空
    # if body['name'] == '' or body['tscode'] == '':
    #     res['code'] = 1
    #     res['msg'] = "股票名称和代码不能为空!"
    #     return JsonResponse(res)
    # else:
    #     gupiao_obj = GPList.objects.filter(tscode=body['tscode']).values()
    #     if len(gupiao_obj) == 0:
    #         gupiao = GPList(
    #             tscode = body['tscode'],
    #             name = body['name'],
    #             symbol = body['symbol'],
    #             industry = body['industry'],
    #             list_date = body['list_date'],
    #             remark = body['remark'],
    #         )
    #         gupiao.save()
    #         res['code'] = 200
    #         res['msg'] = "添加成功"
    #         return JsonResponse(res)
    #     else:
    #         res['code'] = 1
    #         res['msg'] = "数据已存在，请勿重复添加"
    #         return JsonResponse(res)
    elif request.method == 'GET':
        symbolP = request.GET.get('symbol') or ""
        pageNumP = int(request.GET.get('pageNum')) or 1
        pageSizeP = int(request.GET.get('pageSize')) or 10
        gupiao_obj = GPList.objects.filter(symbol__contains=symbolP).order_by('symbol').values() 
        gupiao_list = []
        for data in gupiao_obj[(pageNumP -1) * pageSizeP: pageNumP*pageSizeP - 1]:
            gupiao_list.append(data)
        res2['code'] = 200
        res2['msg'] = "查询成功"
        res2['pageNum'] = pageNumP
        res2['pageSize'] = pageSizeP
        res2['count'] = len(gupiao_obj)
        res2['data'] = gupiao_list
        return JsonResponse(res2, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'PUT':
        params = QueryDict(request.body)
        params_str = list(params.items())[0][0] #将获取的QueryDict对象转换为str 类型
        params_dict = eval(params_str) #将str类型转换为字典类型
     
        gupiao=GPList.objects.get(tscode=params_dict.get("tscode"))
        gupiao.industry=params_dict.get("industry")
        gupiao.remark=params_dict.get("remark")
        gupiao.save()
        res['code'] = 200
        res['msg'] = "修改成功"
        return JsonResponse(res)
    elif request.method == 'DELETE':
        id = request.GET.get('tscode')
        gupiao=GPList.objects.filter(tscode=id)
        gupiao.delete()
        res['code'] = 200
        res['msg'] = "删除成功"
        return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)
