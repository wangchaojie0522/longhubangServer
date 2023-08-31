'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-07-10 15:19:23
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-08-30 14:41:55
FilePath: /longhubangServer/myApp/urls.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from django.urls import path
from myApp import views
from myApp import reloadData

urlpatterns = [
    path('gupiao/', views.gupiao),
    path('gupiao/reload/', reloadData.gupiaoRL),
    path('gupiao/k/', reloadData.gupiaoK)
]