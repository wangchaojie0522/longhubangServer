'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2024-01-05 14:28:59
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2024-01-05 16:32:11
FilePath: /longhubangServer/myApp/API/ztData.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from myApp.data.dfcf import stock_zt_pool
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
        "msg": ""
}
def ztList(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        dateS = request.GET.get('date') or ""
        df = stock_zt_pool(dateS)
        gupiao_list = []
        print(df)
        '代码','名称','涨跌幅','最新价','换手率','成交额(百万)','流通市值(百万)',
        '总市值(百万)','封板资金(百万)','首次封板时间','最后封板时间','炸板次数',
        '涨停统计','连板数','所属行业'
        for index, row in df.iterrows():
            gupiao_list.append({
                "code": row['代码'],
                "name": row['名称'],
                "change": row['涨跌幅'],
                "close": row['最新价'],
                "TR": row['换手率'],
                "TV": row['成交额(百万)'],
                "CMV": row['流通市值(百万)'],
                "TMV": row['总市值(百万)'],
                "CBF": row['封板资金(百万)'],
                "FST": row['首次封板时间'],
                "LST": row['最后封板时间'],
                "NFC": row['炸板次数'],
                "NCB": row['连板数'],
                "LUC": row['涨停统计'],
                "industry": row['所属行业'],
            })
        res2['code'] = 200
        res2['msg'] = "查询成功"
        res2['count'] = len(gupiao_list)
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
