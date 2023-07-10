'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-06-06 16:41:38
FilePath: \webserve\myApp\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.db import models

# Create your models here.
class Person(models.Model):
    person_name = models.CharField('姓名', max_length=64, null=False)
    deposit = models.FloatField('存款')
    add_time = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.person_name, self.deposit
    
class Gupiao(models.Model):
    name = models.CharField('股票名称', max_length=16, null=False)
    code = models.CharField('股票代码', max_length=16, primary_key=True, null=False)
    concept = models.CharField('所属概念', max_length=256, null=True)
    business = models.CharField('主营业务', max_length=256, null=True)
    remark = models.CharField('备注', max_length=256, null=True)

    def __str__(self):
        return self.name, self.code, self.concept, self.business, self.remark