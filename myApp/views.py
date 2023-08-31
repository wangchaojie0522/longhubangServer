'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-08-31 16:32:30
FilePath: \webserve\myApp\views.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse, QueryDict
from django.http.response import HttpResponse
import json

from .models import GPList


# Create your views here.
res2 =  {
        "code": 0,
        "data": [],
        "count": 0,
        "pageSize": 10,
        "pageNum": 1,
        "msg": ""
}
res =  {
        "code": 0,
        "data": [],
        "msg": ""
}
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
