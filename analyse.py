from getdata import *
import matplotlib.pyplot as plt
import sys
import datetime
from darts import TimeSeries


def tserie_analyse():
    df = get_data("GOOGL") 

    start = datetime.datetime.strptime("1973-01-01", "%Y-%m-%d") #把一个时间字符串解析为时间元组
    date_list = [start + relativedelta(months=x) for x in range(0,114)]  #从1973-01-01开始逐月增加组成list
    df['index'] =date_list
    df.set_index(['index'], inplace=True)
    df.index.name=None
    df.columns= ['riders']
    df['riders'] = df.riders.apply(lambda x: int(x)*100)
    df.riders.plot(figsize=(12,8), title= 'Monthly Ridership', fontsize=14)
    #df = df[['close']]


if __name__ == "__main__":
    # print(sys.executable)
    df = get_data("GOOGL")  
    print(df.head())
