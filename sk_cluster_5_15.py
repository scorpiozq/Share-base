# -*- coding: utf-8 -*-
"""
Created on Wed May 15 20:53:53 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.decomposition import PCA

class normlize():
    # 定义一个日期和时间的最小点
    mindate='2019-02-09 00:00:00'
    # 转化成datetime格式
    global mindate_d
    mindate_d=datetime.strptime(mindate,'%Y-%m-%d %H:%M:%S')
    print('mindate_d=',mindate_d)
    
    def n_date(b_time):
        # 聚类期间总共的天数，这个是我自己计算的，后面可能有更好的办法 
        maxdays=80
        #b_date=[]
        date_delta=b_time-mindate_d
        b_date=(date_delta.days)/maxdays
        return b_date
    
    def n_sec(b_time):
        # 一天总共的秒数
        maxsecs=60*60*24        
        #b_second=[]
        sec_delta=b_time-mindate_d
        b_second=(sec_delta.seconds)/maxsecs
        return b_second
    
def main():
    df0=pd.read_csv('F:\AI\Pythonlearning\code\orderid__addtime__total_price.csv',header=None)
    # 更换列索引
    columns=['order_id','addtime','total_price']
    df0.columns=columns
    #print(df0)
    
    # 简单的清洗价格中不合理的部分
    df1=df0[(df0['total_price']<5000)&(df0['total_price']>0)]
    #print(df1[100:105])
    
    # 刚才删去的数据依旧占据着索引，用reset_index来重置索引
    df2=df1.dropna(subset=['total_price']).reset_index(drop=True)
    #df1=df1[df0['total_price']>0]
    #print(df2[100:105])
    
    # 取得下单时间
    b=df2['addtime']

    # 价格归一化
    price_norm=(df2['total_price'] - df2['total_price'].min()) / (df2['total_price'].max() - df2['total_price'].min())
    #z=df2.total_price
    #print(price_norm[1])
    
    # 初始化
    b_t=[]
    b_nd=[]
    b_ns=[]
    b_week=[]
    b_price=[]
    
    # 转化成datetime格式，并进行标准化
    for i in range(8090):
            # 将b字符型转化为datetime
            b_t.append(datetime.strptime(b[i],'%Y-%m-%d %H:%M:%S'))
            # 将 日期和小时标准化
            b_nd.append(normlize.n_date(b_t[i]))
            b_ns.append(normlize.n_sec(b_t[i]))
            # 日期转化为星期
            b_week.append((int(b_t[i].strftime("%w"))+1)/7)
            # 将价格转成array格式
            b_price.append(price_norm[i])

    # 合并成一个4列的array
    np_n=np.c_[b_nd,b_price]#b_ns,,b_week
    #print(np_n[106])
    # 获得KMeans聚类的结果，之后用来作为颜色标签
    y_pred = KMeans(n_clusters=3, random_state=1).fit_predict(np_n)
    
    # 另一种获得颜色标签的方式
    y_fit=KMeans(n_clusters=3, random_state=1).fit(np_n)
    # fit.labels=fit_predict
    
    #print('y_fit.labels_=',y_fit.labels_,'y_pred=',y_pred)
    cluster_lables=pd.DataFrame(y_pred)
    # 字段重命名
    cluster_lables.columns=['lables']
    #print(type(cluster_lables))
    
    # 输出聚类中心点坐标
    print(y_fit.cluster_centers_)
    
    # 将标签和源数据合并输出
    df4=df2.join(cluster_lables)
    #print(df4)
    df4.to_csv('F:\AI\Pythonlearning\code\let_me_see3.csv')
    
    # 用来可视化的dataframe
    df5=pd.DataFrame(np_n)
    columns=['date','total_price']#,'hour','week'
    df5.columns=columns
    #print(df5)
    df6=df5.join(cluster_lables)
    #print(df6)
   
    # 将数据降维至2维
    pca = PCA(n_components=2)
    new_pca = pd.DataFrame(pca.fit_transform(df6))
    #print(new_pca)
    
    # 可视化，用lables标记颜色
    d = new_pca[df6['lables'] == 0]
    plt.plot(d[0], d[1], 'r.')
    d = new_pca[df6['lables'] == 1]
    plt.plot(d[0], d[1], 'go')
    d = new_pca[df6['lables'] == 2]
    plt.plot(d[0], d[1], 'b*')
    plt.gcf().savefig('kmeans.png')
    plt.show()

    # c表示颜色信息
    # 二维散点图
    #plt.scatter(np_n[:,0],np_n[:,1] ,c=y_pred)
    #plt.title("Date and Seconds")
    #plt.show
    
    '''
    # 三维散点图
    ax = plt.axes(projection='3d')
    ax.scatter3D(np_n[:,0], np_n[:,1], np_n[:,2], c=y_pred, cmap='Greens')
    #plt.subplot(211)
    
    plt.show
    '''
if __name__=='__main__':
    main()