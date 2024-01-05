
import requests
import pandas as pd
import requests
 


#涨停股池
def stock_zt_pool(date= None) :
    if date is None:
        date=''
    url = 'http://push2ex.eastmoney.com/getTopicZTPool'
    params = {
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'dpt': 'wz.ztzt',
        'Pageindex': '0',
        'pagesize': '10000',
        'sort': 'fbt:asc',
        'date': date,
        '_': '1621590489736',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json['data'] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json['data']['pool'])
    if len(temp_df) ==0 :
       return 
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    old_cols=['序号','代码','_','名称','最新价','涨跌幅','成交额(百万)','流通市值(百万)',
        '总市值(百万)', '换手率','连板数','首次封板时间','最后封板时间',
        '封板资金(百万)','炸板次数','所属行业','涨停统计',]
    temp_df.columns =  old_cols
    temp_df['涨停统计'] = (temp_df['涨停统计'].apply(lambda x: dict(x)['days']
                ).astype(str) + "/" + temp_df['涨停统计']
               .apply(lambda x: dict(x)['ct']).astype(str))
    new_cols=['代码','名称','涨跌幅','最新价','换手率','成交额(百万)','流通市值(百万)',
        '总市值(百万)','封板资金(百万)','首次封板时间','最后封板时间','炸板次数',
        '涨停统计','连板数','所属行业',]
    df = temp_df[new_cols].copy()
    df['首次封板时间'] = df['首次封板时间'].apply(lambda s:str(s)[-6:-4]+':'+str(s)[-4:-2])
    df['最后封板时间'] = df['最后封板时间'].apply(lambda s:str(s)[-6:-4]+':'+str(s)[-4:-2])
    df['最新价'] = df['最新价'] / 1000
    
    # 将object类型转为数值型
    ignore_cols = ['代码','名称','最新价','首次封板时间','最后封板时间','涨停统计','所属行业',]
    df = trans_num(df, ignore_cols)
    df[['成交额(百万)','流通市值(百万)','总市值(百万)','封板资金(百万)']]=(df[['成交额(百万)',
        '流通市值(百万)','总市值(百万)','封板资金(百万)']]/1000000)
    return df.round(3)

#跌停股池

def stock_dt_pool(date = None):
    """
    获取东方财富网跌停股池
    http://quote.eastmoney.com/ztb/detail#type=dtgc
    date: 交易日
    """
    if date is None:
        date=''
    url = 'http://push2ex.eastmoney.com/getTopicDTPool'
    params = {
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'dpt': 'wz.ztzt',
        'Pageindex': '0',
        'pagesize': '10000',
        'sort': 'fund:asc',
        'date': date,
        '_': '1621590489736',
    }
    res = requests.get(url, params=params)
    data_json = res.json()
    if data_json['data'] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json['data']['pool'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    old_cols=['序号','代码','_','名称','最新价','涨跌幅','成交额(百万)','流通市值(百万)',
        '总市值(百万)','动态市盈率','换手率','封板资金(百万)','最后封板时间','板上成交额',
        '连续跌停','开板次数','所属行业',]
    temp_df.columns = old_cols
    new_cols=['代码','名称','涨跌幅','最新价','换手率','最后封板时间',
        '连续跌停','开板次数','所属行业','成交额(百万)','封板资金(百万)','流通市值(百万)',
        '总市值(百万)']
    df = temp_df[new_cols].copy()
    df['最新价'] = df['最新价'] / 1000
    df['最后封板时间'] = df['最后封板时间'].apply(lambda s:str(s)[-6:-4]+':'+str(s)[-4:-2])
    # 将object类型转为数值型
    ignore_cols = ['代码','名称','最新价','最后封板时间','所属行业',]
    df = trans_num(df, ignore_cols)
    df[['成交额(百万)','流通市值(百万)','总市值(百万)','封板资金(百万)']]=(df[['成交额(百万)',
        '流通市值(百万)','总市值(百万)','封板资金(百万)']]/1000000)
    return df.round(3)

def stock_strong_pool(date= None) :
    """
    获取东方财富网强势股池
    date：日期
    """
    if date is None:
        date=''
    url = 'http://push2ex.eastmoney.com/getTopicQSPool'
    params = {
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'dpt': 'wz.ztzt',
        'Pageindex': '0',
        'pagesize': '170',
        'sort': 'zdp:desc',
        'date': date,
        '_': '1621590489736',
    }
    res = requests.get(url, params=params)
    data_json = res.json()
    if data_json['data'] is None:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json['data']['pool'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    old_cols=['序号','代码','_','名称','最新价','涨停价','_','涨跌幅',
        '成交额(百万)','流通市值(百万)','总市值(百万)', '换手率','是否新高','入选理由',
        '量比','涨速','涨停统计','所属行业',]
    temp_df.columns = old_cols
    temp_df['涨停统计'] = temp_df['涨停统计'].apply(lambda x: dict(x)['days']).astype(str) + "/" + temp_df['涨停统计'].apply(lambda x: dict(x)['ct']).astype(str)
    new_cols=['代码','名称','涨跌幅','最新价','涨停价','换手率','涨速','是否新高','量比',
              '涨停统计','入选理由','所属行业','成交额(百万)','流通市值(百万)','总市值(百万)', ]
    df = temp_df[new_cols].copy()
    df[['最新价','涨停价']] = df[['最新价','涨停价']] / 1000
    df[['成交额(百万)','流通市值(百万)','总市值(百万)']]=(df[['成交额(百万)',
        '流通市值(百万)','总市值(百万)']]/1000000)
    rr={1: '60日新高', 2: '近期多次涨停', 3: '60日新高且近期多次涨停'}
    df['入选理由']=df['入选理由'].apply(lambda s: rr[s])
    return df.round(2)

def trans_num(df, ignore_cols):
    '''df为需要转换数据类型的dataframe
    ignore_cols为dataframe中忽略要转换的列名的list
    如ignore_cols=['代码','名称','所处行业']
    '''
    trans_cols = list(set(df.columns) - set(ignore_cols))
    df[trans_cols] = df[trans_cols].apply(lambda s: pd.to_numeric(s, errors='coerce'))
    return df
def is_trading_day(date):
    # 定义第三方API的URL和参数
    url = 'https://api.website.com/is_trading_day'
    payload = {'date': date}
 
    # 发送GET请求判断当前日期是否是交易日
    response = requests.get(url, params=payload)
    if response.status_code == 200:
        result = response.json()
        if result['is_trading_day']:
            return True
    return False
