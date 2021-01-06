import tushare as ts
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib.pylab import date2num
from sqlalchemy import create_engine
from dateutil.parser import parse  ## 导入转换到指定格式日期的工具

def gupiao(num):
    lingyi = ts.get_hist_data(num,start='2020-01-01',end='2020-06-25')
    to_mysql(lingyi)
    l = lingyi.copy()
    l.reset_index(inplace=True)  # 重设index,原来的index汇入DataFrame中
    l.index = pd.to_datetime(l.date)  # 设置index的值
    date = pd.DataFrame(lingyi.axes)[0]
    data = lingyi.loc[:, ['open', 'close', 'high', 'low']]
    da = l.loc[:, ['date', 'open', 'close', 'high', 'low']]
    da['date'] = da['date'].apply(lambda x: date2num(datetime.datetime.strptime(x, '%Y-%m-%d')))
    # 由于使用的是限定格式的数据，需转换成以下格式
    f = da[['date', 'open', 'close', 'high', 'low']].values

    plt.rcParams['font.family'] = 'SimHei'  ## 设置字体
    # fig, ax = plt.subplots() ## 创建图片和坐标轴
    fig, ax = plt.subplots(figsize=(1200 / 72, 480 / 72))
    fig.subplots_adjust(bottom=0.2)  ## 调整底部距离
    ax.xaxis_date()  ## 设置X轴刻度为日期时间
    plt.xticks(rotation=45)  ## 设置X轴刻度线并旋转45度
    plt.yticks()  ## 设置Y轴刻度线
    plt.title(str(num))  ##设置图片标题
    plt.xlabel(u"时间")  ##设置X轴标题
    plt.ylabel(u"股价（元）")  ##设置Y轴标题
    plt.grid(True, 'major', 'both', ls='--', lw=.5, c='k', alpha=.3)  ##设置网格线

    mpf.candlestick_ochl(ax, f, colordown='#53c156', colorup='#ff1717', width=0.3, alpha=1)
    plt.show()

def to_mysql(data):
    yconnect = create_engine('mysql+mysqldb://root:123@localhost:3306/gupiao?charset=utf8')
    pd.io.sql.to_sql(data, 'data', yconnect, schema='gupiao', if_exists='append')

w = tk.Tk()
w.title('股票查询系统')  # 主窗口标题
w.geometry('300x300')  # 窗口尺寸
frame = tk.Frame(w)
frame.pack()
frame_l = tk.Frame(frame)
frame_r = tk.Frame(frame)
frame_l.pack(side='left')
frame_r.pack(side='right')
tk.Label(frame_l,text='请输入你要查询的股票代码      ').pack()
num = tk.Entry(frame_r, show=None)
num.pack()
b1 = tk.Button(w, text='确定', width=15, height=2, command=lambda:gupiao(num.get()))
b1.pack()
tk.mainloop()