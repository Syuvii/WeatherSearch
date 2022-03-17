import re
import requests
from bs4 import BeautifulSoup

class WeaInfo():
    #初始化
    def __init__(self,city) -> None:
        self.city = city
        self.code = 1
        try :
            if self.get_id()==False:
                self.code = 0
                return None
        except Exception:
            self.code = -1
            return None
        
        id = self.get_id()['id']
        self.city_name = self.get_id()['name']
        data_url = 'http://www.weather.com.cn/weathern/%s.shtml'%id
        old_url = 'http://www.weather.com.cn/weather/%s.shtml'%id  
        response = requests.get(data_url)
        response.encoding = 'UTF-8'
        self.soup = BeautifulSoup(response.text,'lxml')
        response_o = requests.get(old_url)
        response_o.encoding = 'UTF-8'
        self.soup_o = BeautifulSoup(response_o.text,'lxml')
    #获取城市id
    def get_id(self):
        url = 'https://geoapi.qweather.com/v2/city/lookup'
        params = {
            'location':self.city,
            'key':'e84beef343864b5da760d356b55d934f',
            'range':'cn',
            'number':'1'
            }
        locationid = requests.get(url,params).json()
        if locationid['code']!='200':
            return False 
        else:
            return locationid['location'][0]
    #获取温度和日出日落信息           
    def get_tem_sun(self):
        tem = self.soup.select('body > div.L_weather > div.fl.weather_left > div.weather_7d > div > script')
        text = str(tem)
        def list_trans(temp,type):
            return list(map(type,temp.group(1).replace('"','',16).split(',')))
        sunup = re.search( r"sunup =\[(.*?)\];$", text, re.M|re.I)
        sunset = re.search( r"sunset =\[(.*?)\];$", text, re.M|re.I)
        sunup = list_trans(sunup,str)
        sunset = list_trans(sunset,str)
        max_7 = re.search( r"eventDay =\[(.*?)\];$", text, re.M|re.I)
        min_7 = re.search( r"eventNight =\[(.*?)\];$", text, re.M|re.I)
        t_max_7 = list_trans(max_7,int)
        t_min_7 = list_trans(min_7,int)
        max_15 = re.search( r"fifDay =\[(.*?)\];$", text, re.M|re.I)
        min_15 = re.search( r"fifNight =\[(.*?)\];$", text, re.M|re.I)
        t_max_15 = list_trans(max_15,int)
        t_min_15 = list_trans(min_15,int)
        return t_max_7+t_max_15,t_min_7+t_min_15,sunup,sunset
    #获取天气情况 
    def get_wea(self):
        wea = self.soup.select('.weather-info')
        text = str(wea)
        pattern = re.compile( r">(.*?)</p>")
        temp = pattern.findall(text)
        return temp
    #获取风向风力
    def get_win(self):
        win_dt = self.soup.select('.wind-container')
        win_pow = self.soup.select('.wind-info')
        text_d = str(win_dt)
        text_p = str(win_pow)
       
        pattern_d = re.compile(r'title="(.*?)"')
        pattern_p = re.compile(r'">(.*?)</p>')
        temp_d = pattern_d.findall(text_d)  
        temp_p = pattern_p.findall(text_p)[:8]
        for i in range(8):            
            temp_p[i]=temp_p[i].replace('&lt;','<')
        return list(zip([temp_d[i] for i in range(0,len(temp_d),2)],
                        [temp_d[i] for i in range(1,len(temp_d),2)],
                        [temp_p[i]for i in range(len(temp_p))]))
    #获取tips
    def get_suge(self):
        result = []
        suge = self.soup_o.find('div',attrs={'class':'hide show'}).find_all('p')
        for data in suge:
            temp = list(data.get_text())
            for i in range(1,len(temp)):
                if i % 10 ==0:
                    temp.insert(i,'\n')
            result.append(''.join(temp))
        
        return result
    #获取整点气温情况
    def get_tem_int(self):
        temp = self.soup.find('div',attrs={'class':'details-container'}).find('script')
        text = str(temp)
        pattern = re.compile( r'"jb":"(.*?)"')
        temp = pattern.findall(text)[:24]
        t_int = list(map(int,temp))
        return t_int
    #获取空气质量，相对湿度，时间
    def get_aqi_hd_date(self):
        temp = self.soup_o.select('body > div.con.today.clearfix > div.left.fl > div:nth-child(3) > script')
        text = str(temp)
        pattern_a = re.compile( r'"od28":"(.*?)"'); pattern_h = re.compile( r'"od27":"(.*?)"'); pattern_d = re.compile( r'"od21":"(.*?)"')
        temp_a = pattern_a.findall(text); temp_h = pattern_h.findall(text); temp_d = pattern_d.findall(text)
        temp_a = ['0' if i == ''else i for i in temp_a]
        temp_a.reverse(); temp_h.reverse(); temp_d.reverse()
        temp_a.pop(); temp_h.pop(); temp_d.pop()
        temp_a = list(map(int,temp_a));temp_h = list(map(int,temp_h));temp_d = list(map(str,temp_d))
        return temp_a,temp_h,temp_d
