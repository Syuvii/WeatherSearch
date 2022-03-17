import re
import numpy as np
from matplotlib import pyplot as plt

def get_tem_pic(date,t_max,t_min):
    plt.figure(figsize=(8,4),dpi=100)
    plt.rcParams["font.family"]="SimHei"
    plt.title("近15天气温趋势图") 
    plt.xlabel("日期/日") 
    plt.ylabel("温度/℃") 
    plt.plot(date,t_max, 'or-',date,t_min,'ob:')
    for a,b in zip(date,t_max):
        plt.text(a, b+0.5, '%d℃' % b, ha='center', va= 'bottom',fontsize=10)
    for a,b in zip(date,t_min):
        plt.text(a, b+0.5, '%d℃' % b, ha='center', va= 'bottom',fontsize=10)
    plt.ylim(10,40)
    plt.grid(axis='x')
    plt.savefig('image/vslz/tem_15.png')

def get_tem_bar_pic(date,t_max,t_min):
    x_range = np.arange(len(date))
    plt.figure(figsize=(8,4),dpi=100)
    plt.rcParams["font.family"]="SimHei"
    plt.title("近15天气温趋势图") 
    plt.xlabel("日期/日") 
    plt.ylabel("温度/℃") 
    plt.bar(x_range+0.2,t_max,color = 'r',width=0.4,tick_label = date)
    plt.bar(x_range-0.2,t_min,color = 'b',width=0.4,tick_label = date)
    for a,b in zip(x_range,t_max):
        plt.text(a+0.2, b+0.5, '%d℃' % b, ha='center', va= 'bottom',fontsize=8)
    for a,b in zip(x_range,t_min):
        plt.text(a-0.2, b+0.5, '%d℃' % b, ha='center', va= 'bottom',fontsize=8)
    plt.savefig('image/vslz/tem_15_bar.png')

def get_pic(x,y,x_label,y_label,title,name,dm='',y_min=0,y_max=0,size = 10):
    plt.figure(figsize=(8,4),dpi=100)
    plt.rcParams["font.family"]="SimHei"
    plt.rcParams['axes.unicode_minus'] =False
    plt.title(title) 
    plt.xlabel(x_label) 
    plt.ylabel(y_label) 
    plt.plot(x,y, 'or-')
    for a,b in zip(x,y):
        plt.text(a, b+0.5, '%d%s' % (b,dm), ha='center', va= 'bottom',fontsize=size)
    if y_min !=0:
        plt.ylim(y_min,y_max)
    plt.grid(axis='x')
    plt.savefig('image/vslz/'+name)

def get_bar_pic(x,y,x_label,y_label,title,name,dm='',size=10):
    x_range = np.arange(len(x))
    plt.figure(figsize=(8,4),dpi=100)
    plt.rcParams["font.family"]="SimHei"
    plt.title(title) 
    plt.xlabel(x_label) 
    plt.ylabel(y_label) 
    plt.bar(x_range,y,tick_label = x)
    for a,b in zip(x_range,y):
        plt.text(a, b+0.5, '%d%s' % (b,dm), ha='center', va= 'bottom',fontsize=size)
    plt.savefig('image/vslz/'+name)

def get_tem_int_pic(date,t_int):
    get_pic(date,t_int,'时间/时','温度/℃',"近24h气温趋势图",'tem_int.png','℃',size=9)
    get_bar_pic(date,t_int,'时间/时','温度/℃',"近24h气温趋势图",'tem_int_bar.png','℃',8)

def get_aqi_pic(date,aqi):
    get_pic(date,aqi,'时间/时','空气指数',"近24h空气质量指数",'aqi.png')
    get_bar_pic(date,aqi,'时间/时','空气指数',"近24h空气质量指数",'aqi_bar.png')

def get_hd_pic(date,hd):
    get_pic(date,hd,'时间/时','相对湿度',"近24h相对湿度",'hd.png','%')
    get_bar_pic(date,hd,'时间/时','相对湿度',"近24h相对湿度",'hd_bar.png','%')

def get_des(wea_des):
    pattern = re.compile(r'(.*?)转(.+?)$')
    # wea = '晴转多云'
    temp = re.findall(pattern,wea_des)
    if len(temp)==0:
        return wea_des,wea_des
    else:
        return temp[0] 
        