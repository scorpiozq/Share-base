# -*- coding: utf-8 -*-
"""
Created on Sun May  5 19:37:27 2019

@author: Administrator
"""

import math
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from copy import copy

# 更新中心点
def new(group):
    minimum=10000
    o=[]
    for x1 in group['x']:
        for y1 in group['y']:
            j=0
            red_sum=0
            # 遍历每个点，x和y的长度相同
            while j<=len(group['x'])-1:
                # 计算每个x1，y1到所有点距离的和
                red_sum+=math.sqrt((group['x'][j]-x1)**2+(group['y'][j]-y1)**2)
                j+=1
            o.append(red_sum)
            #print('o=',o)
            # 如果此时的距离和最小
            if(red_sum<minimum):
                # 则此时的距离最小值替换为这根sum,将中心点换成此时的x和y
                minimum=copy(red_sum)
                x2=copy(x1)
                y2=copy(y1)
                #print(x2,y2)    
    return x2,y2

# 给所有数据着色
def color(a,b_timestamp,x,y):
    # 初始化循环次数
    i=0
    # 定义一个字典存储三个颜色的数据有哪些
    red={'x':[],'y':[]}
    blue={'x':[],'y':[]}
    black={'x':[],'y':[]}
    # 进入循环将每个数据赋予颜色
    while i<=107:
        # 计算每个数据点距离两个随机点的距离
        #print(int(b_timestamp[i]))
        distance0=math.sqrt((int(a[i])-x[0])**2+(int(b_timestamp[i])-y[0])**2)
        distance1=math.sqrt((int(a[i])-x[1])**2+(int(b_timestamp[i])-y[1])**2)
        distance2=math.sqrt((int(a[i])-x[2])**2+(int(b_timestamp[i])-y[2])**2)
        # 将这些的颜色变为离他最近的随机点对应的颜色
        if (min(distance0,distance1,distance2)==distance0):
            plt.plot(a[i],b_timestamp[i],'ro',color='red')
            red['x'].append(int(a[i]))
            red['y'].append(int(b_timestamp[i]))
        elif (min(distance0,distance1,distance2)==distance1):
            plt.plot(a[i],b_timestamp[i],'ro',color='blue')
            blue['x'].append(int(a[i]))
            blue['y'].append(int(b_timestamp[i]))
        else:
            plt.plot(a[i],b_timestamp[i],'ro',color='black')
            black['x'].append(int(a[i]))
            black['y'].append(int(b_timestamp[i]))
        i+=1
    # 返回一个字典，里面存储了三个颜色对应的点
    return red,blue,black

def main():
    # 将时间订单表导入，参数标题为无
    df1=pd.read_csv('G:\AI\Pythonlearning\code\order_id and addtime.csv',header=None)
    # 赋值a为订单id,b为时间
    a=df1[0]# 订单ID
    b=df1[2]# 下单时间
    b_timearray=[]
    b_timestamp=[]
    #print(type(b[1]))
    
    for i in range(0,108):
        b_timearray.append(time.strptime(b[i],"%Y-%m-%d %H:%M:%S"))
        b_inter=(int(time.mktime(b_timearray[i])))/10**6
        b_timestamp.append(b_inter)
        #print(a,b,sep="\n")
    # 初始化x,y为随机坐标
    x=[random.randint(1,50),random.randint(1,50),random.randint(1,50)]
    y=[random.randint(155*10,155.2*10),random.randint(155*10,155.2*10),
       random.randint(155*10,155.2*10)]
    print("初始随机中心点坐标为")
    print(x,y,sep="\n")
    # 将所有数据点着色
    red,blue,black=color(a,b_timestamp,x,y)
    # 将随机的两个点着色并用X强调显示
    #plt.plot(x,y,'go',color="green")
    plt.plot(x[0],y[0],'x',color='red',markersize=15)
    plt.plot(x[1],y[1],'x',color='blue',markersize=15)
    plt.plot(x[2],y[2],'x',color='black',markersize =15)
    plt.show()
    #plt.axis([0,25,0,25])
    '''
    print ('length=',len(red['x']))
    for item in red.items():
        print(item)
    print(new(red))
    '''   
    print("检查旧的中心点和新的中心点是否相等")
    while ((x[0],y[0])!=new(red)) or ((x[1],y[1])!=new(blue)) \
    or ((x[2],y[2])!=new(black)):
        #print(new(red))
        
        print('*********\n',x[0],y[0],new(red),'\n',
              x[1],y[1],new(blue),'\n',x[2],y[2],new(black),'\n*********\n')
        x[0],y[0]=new(red)      
        x[1],y[1]=new(blue)
        x[2],y[2]=new(black)
        # 不相等，重新着色
        red,blue,black=color(a,b_timestamp,x,y) 

        plt.plot(x[0],y[0],'x',color='red',markersize=15)
        plt.plot(x[1],y[1],'x',color='blue',markersize=15)
        plt.plot(x[2],y[2],'x',color='black',markersize=15)
        plt.show()

if __name__=='__main__':
    main()