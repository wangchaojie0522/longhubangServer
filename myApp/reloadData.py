'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-08-30 15:43:31
FilePath: \webserve\myApp\views.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.http import JsonResponse

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
def gupiaoRL(request):
    
    if request.method == 'POST':
        res['code'] = 200
        res['msg'] = "数据库已更新!"
        return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = "request method not is require!"
        return JsonResponse(res)