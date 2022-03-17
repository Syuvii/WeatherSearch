import sys
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QCloseEvent, QPalette, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QDialog, QFrame, QMessageBox, QWidget, QApplication, \
    QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, QPushButton, QLineEdit
class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.code = 0
        self.file_name = 'id_pwd.json'
        self.initUI()
 
    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.setObjectName("loginWindow")
        self.setStyleSheet('#loginWindow{background-color:white}')
        self.setFixedSize(400, 300)
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon('image/icon.ico'))

    
        # 添加顶部logo图片
        pixmap = QPixmap("image/login_back")
        scaredPixmap = pixmap.scaled(400, 100)
        label = QLabel(self)
        label.setPixmap(scaredPixmap)
    
        # 登录表单内容部分
        login_widget = QWidget(self)
        # login_widget.move(0, 140)
        login_widget.setGeometry(0, 100, 400, 200)
    
        hbox = QHBoxLayout()
        h_box = QHBoxLayout()
        # 添加右侧表单
        fmlayout = QFormLayout()
        lbl_workerid = QLabel("用户名")
        lbl_workerid.setFont(QFont("Microsoft YaHei"))
        self.led_workerid = QLineEdit()
        self.led_workerid.setFixedWidth(270)
        self.led_workerid.setFixedHeight(38)
    
        lbl_pwd = QLabel("密码")
        lbl_pwd.setFont(QFont("Microsoft YaHei"))
        self.led_pwd = QLineEdit()
        self.led_pwd.setEchoMode(QLineEdit.Password)
        self.led_pwd.setFixedWidth(270)
        self.led_pwd.setFixedHeight(38)
    
        btn_login = QPushButton("登录")
        btn_login.setFixedWidth(100)
        btn_login.setFixedHeight(40)
        btn_login.setFont(QFont("Microsoft YaHei"))
        btn_login.setObjectName("login_btn")
        btn_login.setStyleSheet("#login_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")
        btn_login.clicked.connect(self.check_login_func)

        btn_signup = QPushButton("注册")
        btn_signup.setFixedWidth(100)
        btn_signup.setFixedHeight(40)
        btn_signup.setFont(QFont("Microsoft YaHei"))
        btn_signup.setObjectName("signup_btn")
        btn_signup.setStyleSheet("#signup_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")
        btn_signup.clicked.connect(self.sign_up)

        btn_quit = QPushButton("退出")
        btn_quit.setFixedWidth(100)
        btn_quit.setFixedHeight(40)
        btn_quit.setFont(QFont("Microsoft YaHei"))
        btn_quit.setObjectName("quit_btn")
        btn_quit.setStyleSheet("#quit_btn{background-color:#2c7adf;color:#fff;border:none;border-radius:4px;}")
        btn_quit.clicked.connect(sys.exit)

        h_box.addWidget(btn_login)
        h_box.addWidget(btn_signup)
        h_box.addWidget(btn_quit)
        h_box.setAlignment(Qt.AlignCenter)
        h_box.setSpacing(20)
        fmlayout.addRow(lbl_workerid, self.led_workerid)
        fmlayout.addRow(lbl_pwd, self.led_pwd)
        fmlayout.addRow(h_box)
        hbox.setAlignment(Qt.AlignCenter)
        # 调整间距
        fmlayout.setHorizontalSpacing(20)
        fmlayout.setVerticalSpacing(12)
        hbox.addLayout(fmlayout, 2)
        login_widget.setLayout(hbox)
        self.show()

    def check_login_func(self):
        with open ('id_pwd.json','r') as r_obj:
            USER_PWD = json.load(r_obj)
        if USER_PWD.get(self.led_workerid.text()) == self.led_pwd.text():
            # QMessageBox.critical(self, 'Wrong', '用户名或密码错误!')
            # return
            self.accept()
            self.close()
        else:
            QMessageBox.critical(self, 'Wrong', '用户名或密码错误!')

            self.led_workerid.clear()
            self.led_pwd.clear()

    def sign_up(self):
        if self.code == 0:
            self.led_workerid.clear()
            self.led_pwd.clear()
            self.code = 1
            QMessageBox.information(self, '开始注册', '输入完成后再次点击注册')    
        elif self.code == 1:
            id = self.led_workerid.text()
            pwd = self.led_pwd.text()
            with open("id_pwd.json",'r') as load_f:
                 load_dict = json.load(load_f)
            if id in load_dict.keys():
                QMessageBox.information(self, '该账号已存在', '请输入密码登录')
                self.led_pwd.clear()
            else:
                load_dict[id]=pwd
                with open("id_pwd.json","w") as dump_f:
                    json.dump(load_dict,dump_f)
                self.code = 0               
                QMessageBox.information(self, '注册成功', '现在可直接登录')
