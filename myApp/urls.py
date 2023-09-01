'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-07-10 15:19:23
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-09-01 12:54:28
FilePath: /longhubangServer/myApp/urls.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from django.urls import path
from myApp.API import gpData
from myApp.API import etfData

urlpatterns = [
    path('gupiao/list/', gpData.gupiao),
    path('gupiao/reload/', gpData.gupiaoRL),
    path('gupiao/kinfo/', gpData.gupiaoKInfo),
    path('etf/list/', etfData.etf),
    path('etf/reload/', etfData.etfRL),
    path('etf/kinfo/', etfData.etfKInfo),
]