# coding:utf-8
import datetime
from functions import*
from weainfo import *
from login import *
import sys
#搜索界面ui
class MainUi(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setFixedSize(400,150)
        self.setWindowTitle('天气查询')
        self.setWindowIcon(QIcon('image/icon.ico'))
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)#去边框
        self.search = QLineEdit(self)
        self.search.setGeometry(25,50,225,50)
        self.search.setPlaceholderText("请输入城市名进行查询")
        self.search.setFont(QFont('Roman times',12))
        self.search.setStyleSheet(
        '''QLineEdit{
        border:1px solid gray;
        width:300px;
        border-radius:20px;
        padding:2px 4px;
        }''')
        
        self.findButton = QPushButton('查询',self)
        self.findButton.setGeometry(250,50,50,50)
        self.findButton.clicked.connect(self.find_weather)
        self.findButton.setShortcut(QApplication.translate('Widget','Return'))
        self.findButton.setStyleSheet('background-color: rgb(2,179,64);border-radius:25px;')


        self.quitButton = QPushButton('退出',self)
        self.quitButton.setGeometry(300,50,50,50)
        self.quitButton.clicked.connect(self.close)
        self.quitButton.setShortcut(QApplication.translate('Widget','Escape'))
        self.quitButton.setStyleSheet('background-color: rgb(255,79,122);border-radius:25px;')

    def find_weather(self):
        city = self.search.text()
        weainfo = WeaInfo(city)
        if weainfo.code == 1:
            showui.show_details(weainfo)
        elif weainfo.code == 0:
            self.wrong()
        elif weainfo.code == -1:
            self.net_err()

    def net_err(self):       
        QMessageBox.information(self, '查询失败',
                                '网络异常，请检查网络重试',
                                QMessageBox.Yes |QMessageBox.Yes)

    def wrong(self):       
        QMessageBox.information(self, '查询失败',
                                '输入城市无查询结果，请重新输入',
                                QMessageBox.Yes |QMessageBox.Yes)
#展示界面ui
class ShowUi(QWidget):
    def __init__(self):
        super().__init__()
        self.list_l = []
        self.list_p = []
        path = 'image/vslz/'
        
        self.pic_total = [(path+'tem_15.png',path+'tem_15_bar.png'),
                        (path+'tem_int.png',path+'tem_int_bar.png'),
                        (path+'aqi.png',path+'aqi_bar.png'),
                        (path+'hd.png',path+'hd_bar.png')]
        self.count = 1
        self.pic_count = 0
        self.pic_index = 0
        self.more_txt = '时间:{}\n天气: {}\n最高温度:{}℃\n最低温度:{}℃\n风力:{}\n风向:{}'
        self.wea_text = '天气:{}\n最高温/最低温:{}℃/{}℃\n风力:{}\n风向:{}'

    def show_details(self, weainfo):
        self.setStyleSheet("QLabel{color:rgb(255,255,255);}")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("image/background.png")))  
        self.setPalette(palette)
        title = weainfo.city_name + "近7天天气状况"
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon('image/icon.ico'))
        self.setFixedSize(1600,900)
        #自身属性初始化

        t_max,t_min,sunup,sunset = weainfo.get_tem_sun()#日出日落在这
        t_int = weainfo.get_tem_int()
        aqi,hd,date = weainfo.get_aqi_hd_date()
        wea = weainfo.get_wea()
        path_wea = 'image/weaico/%s.png'
        wea_1,wea_2 = get_des(wea[1])
        win = weainfo.get_win()
        self.suge = weainfo.get_suge()
        today = datetime.date.today()
        day = datetime.timedelta(days=1) 
        date_15 = []
        for i in range(16):
            date_15.append((today-day).strftime("%d"))
            today += day  

        today = datetime.date.today()
        date_int = []
        temp = 8
        for i in range(24):
            date_int.append(str(temp).zfill(2))
            temp +=1 
            if temp>23:
                temp = 0

        get_tem_pic(date_15,t_max,t_min)
        get_tem_bar_pic(date_15,t_max,t_min)
        get_aqi_pic(date,aqi)
        get_hd_pic(date,hd)
        get_tem_int_pic(date_int,t_int)
        #画图，初始化要用到的变量

        self.style_Button = QPushButton('更换样式',self)
        self.style_Button.setGeometry(1400,50,100,50)
        self.style_Button.clicked.connect(self.chart_stye_change)

        self.t_15_Button = QPushButton('15天气温图',self)
        self.t_15_Button.setGeometry(700,525,100,50)
        self.t_15_Button.clicked.connect(self.chage_t_15)

        self.t_int_Button = QPushButton('24h气温图',self)
        self.t_int_Button.setGeometry(900,525,100,50)
        self.t_int_Button.clicked.connect(self.change_t_int)

        self.aqi_Button = QPushButton('空气质量',self)
        self.aqi_Button.setGeometry(1100,525,100,50)
        self.aqi_Button.clicked.connect(self.change_aqi)

        self.hd_Button = QPushButton('相对湿度',self)
        self.hd_Button.setGeometry(1300,525,100,50)
        self.hd_Button.clicked.connect(self.change_hd)

        self.suge_Button = QPushButton('下一条提示',self)
        self.suge_Button.setGeometry(350,500,100,50)
        self.suge_Button.clicked.connect(self.suge_double_event)


        lb = QLabel(self)
        lb.setGeometry(50,25,300,50)
        lb.setText('%s今日天气情况:'%weainfo.city_name)
        lb.setFont(QFont('Roman times',20))
        self.list_l.append(lb)
        #lb[0]

        lb = QLabel(self)
        lb.setGeometry(50,400,400,100)
        lb.setFrameShape(QFrame.Box)
        lb.setAlignment(Qt.AlignCenter)
        lb.setText(self.suge[0])
        lb.setFont(QFont('Roman times',20))
        self.list_l.append(lb)
        #lb[1]

        lb = QLabel(self)
        lb.setGeometry(50,550,300,60)
        lb.setText('未来6天天气情况:')
        lb.setFont(QFont('Roman times',20))
        self.list_l.append(lb)
        #lb[2]

        lb = QLabel(self)
        lb.setGeometry(50,125,500,225)
        lb.setText(self.wea_text.format(wea[1],t_max[1],t_min[1],win[1][2],win[1][0]+','+win[1][1]))
        lb.setFrameShape(QFrame.Box)
        lb.setFont(QFont('Roman times',25))
        self.list_l.append(lb)
        #lb[3]

        
        pic = QLabel(self)
        pic.setGeometry(700,100,800,400)
        pic.setScaledContents(True)
        pic.setPixmap(QPixmap('image/vslz/tem_15.png'))
        self.list_p.append(pic)
        #pic[0]
        
        pic = QLabel(self)
        pic.setGeometry(320,0,128,128)
        pic.setScaledContents(True)
        pic.setPixmap(QPixmap(path_wea%wea_1))
        self.list_p.append(pic)
        #pic[1]

        pic = QLabel(self)
        pic.setGeometry(420,0,128,128)
        pic.setScaledContents(True)
        pic.setPixmap(QPixmap(path_wea%wea_2))
        self.list_p.append(pic)
        #pic[2]

        for i in range(2,8):
            lb = QLabel(self)
            lb.setGeometry(75+250*(i-2),650,230,250)
            lb.setText(self.more_txt.format(today+day*(i-1),wea[i],t_max[i],t_min[i],win[i][2],win[i][0]+'\n     '+win[i][1]))
            lb.setFont(QFont('Roman times',15))
            lb.setFrameShape(QFrame.Box)
            lb.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(2,108,124);')
            self.list_l.append(lb)
        #lb[4:9]
        self.show()       

    def closeEvent(self, a0: QCloseEvent) -> None:
        for lb in self.list_l:
            lb.close()
        self.list_l.clear()
        for pic in self.list_p:
            pic.close()
        self.list_p.clear()
        return super().closeEvent(a0)

    def suge_double_event(self,event):
        self.count += 1
        if self.count>5:
            self.count = 0        
        self.list_l[1].setText(self.suge[self.count])

    def chart_stye_change(self,event):
        self.pic_count += 1
        if self.pic_count > 1:
            self.pic_count = 0 
        self.list_p[0].setPixmap(QPixmap(self.pic_total[self.pic_index][self.pic_count]))

    def chage_t_15(self,event):
        self.pic_index = 0
        self.list_p[0].setPixmap(QPixmap(self.pic_total[0][self.pic_count]))

    def change_t_int(self,event):
        self.pic_index = 1
        self.list_p[0].setPixmap(QPixmap(self.pic_total[1][self.pic_count]))

    def change_aqi(self,event):
        self.pic_index = 2
        self.list_p[0].setPixmap(QPixmap(self.pic_total[2][self.pic_count]))

    def change_hd(self,event):
        self.pic_index = 3
        self.list_p[0].setPixmap(QPixmap(self.pic_total[3][self.pic_count]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #登录界面ui
    login = LoginForm()
    if login.exec_()==QDialog.Accepted:
        mainui = MainUi()
        showui = ShowUi()
        sys.exit(app.exec_())

    sys.exit(app.exec_())
