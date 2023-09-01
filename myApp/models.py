'''
Author: chaojiewang chaojiewang@deepglint.com
Date: 2023-06-05 18:37:29
LastEditors: chaojiewang chaojiewang@deepglint.com
LastEditTime: 2023-09-01 13:13:55
FilePath: \webserve\myApp\models.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from django.db import models

# Create your models here.

class GPList(models.Model):
    tscode = models.CharField('股票TS', max_length=16, primary_key=True,null=False)
    name = models.CharField('股票名称', max_length=16, null=False)
    symbol = models.CharField('股票代码', max_length=16,  null=False)
    industry = models.CharField('所属行业', max_length=256, null=True)
    list_date = models.CharField('上市日期', max_length=256, null=True)
    remark = models.CharField('备注', max_length=256, null=True)

    def __str__(self):
        return self.tscode, self.name, self.symbol, self.industry, self.list_date, self.remark
    
class GPdaily(models.Model):
    tscode = models.CharField('股票代码', max_length=16, primary_key=True, null=False)
    trade_date = models.CharField('交易日期', max_length=256, null=True)
    open = models.CharField('开盘价', max_length=256, null=True)
    high = models.CharField('最高价', max_length=256, null=True)
    low = models.CharField('最低价', max_length=256, null=True)
    close = models.CharField('收盘价', max_length=256, null=True)
    pre_close = models.CharField('昨日收盘价', max_length=256, null=True)
    change = models.CharField('涨跌额', max_length=256, null=True)
    pct_chg = models.CharField('涨跌额', max_length=256, null=True)
    vol = models.CharField('成交量（手）', max_length=256, null=True)
    amount = models.CharField('成交额（千元）', max_length=256, null=True)
    def __str__(self):
        return self.tscode, self.trade_date, self.open, self.high, self.low, self.close, self.pre_close, self.change, self.pct_chg, self.vol, self.amount
class ETFList(models.Model):
    tscode = models.CharField('基金代码', max_length=16, primary_key=True,null=False)
    name = models.CharField('简称', max_length=16, null=False)
    management = models.CharField('管理人', max_length=16,  null=False)
    fund_type = models.CharField('投资类型', max_length=256, null=True)
    list_date = models.CharField('上市时间', max_length=256, null=True)
    found_date = models.CharField('成立日期', max_length=256, null=True)
    issue_date = models.CharField('发行日期', max_length=256, null=True)
    issue_amount = models.CharField('发行份额(亿)', max_length=256, null=True)
    invest_type = models.CharField('投资风格', max_length=256, null=True)
    type = models.CharField('基金类型', max_length=256, null=True)
    p_value = models.CharField('面值', max_length=256, null=True)
    def __str__(self):
        return self.tscode, self.name, self.management, self.fund_type, self.found_date, self.issue_date, self.issue_amount, self.invest_type, self.type, self.p_value