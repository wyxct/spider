#!/usr/bin/env python
#coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from mpl import candlestick_ochl
from matplotlib import MultipleLocator
#根据指定代码和时间范围，获取股票数据
df = pd.read_csv('D:/stockData/ch7/600895.csv',encoding='gbk')
#设置大小，共享x坐标轴
figure,(axPrice, axVol) = plt.subplots(2, sharex=True, figsize=(15,8))
#调用方法，绘制K线图
candlestick_ochl(ax = axPrice,          opens=df["Open"].values, closes=df["Close"].values,                 highs=df["High"].values, lows=df["Low"].values,
                 width=0.75, colorup='red', colordown='green')
axPrice.set_title("600895张江高科K线图和均线图")#设置子图标题
df['Close'].rolling(window=3).plot(ax=axPrice,color="red",label='3天均线')
df['Close'].rolling(window=5).plot(ax=axPrice,color="blue",label='5天均线')
df['Close'].rolling(window=10).plot(ax=axPrice,color="green",label='10天均线')
axPrice.legend(loc='best') #绘制图例
axPrice.set_ylabel("价格（单位：元）")
axPrice.grid(True) #带网格线
#如下绘制成交量子图
#直方图表示成交量，用for循环处理不同的颜色
for index, row in df.iterrows():
   if(row['Close'] >= row['Open']):
       axVol.bar(row['Date'],row['Volume']/1000000,width = 0.5,color='red')
   else:
       axVol.bar(row['Date'],row['Volume']/1000000,width = 0.5,color='green')
axVol.set_ylabel("成交量（单位：亿手）")#设置y轴标题
axVol.set_title("600895张江高科成交量")#设置子图的标题
axVol.set_ylim(0,df['Volume'].max()/100000000*1.2)#设置y轴范围
xmajorLocator = MultipleLocator(5) #将x轴主刻度设置为5的倍数
axVol.xaxis.set_major_locator(xmajorLocator)
axVol.grid(True) #带网格线
#旋转x轴的展示文字角度
for xtick in axVol.get_xticklabels():
   xtick.set_rotation(15)
plt.rcParams['font.sans-serif']=['SimHei']
plt.show()