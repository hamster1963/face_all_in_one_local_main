import sqlite3
import sys
import datetime
import threading

import cv2
import pyzbar.pyzbar as pyzbar
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *






class MainUI(object):
    def __init__(self):
        super(MainUI, self).__init__()


    def initUi(self, QMainWindow):
        QMainWindow.setFixedSize(480, 640)  # 640,480

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.main_layout.setSpacing(0)  # 去除控件间隙
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        fontId = QFontDatabase.addApplicationFont(r"/home/linaro/Desktop/ui/SourceHanSans.ttf")
        SourceHanSans = QFontDatabase.applicationFontFamilies(fontId)[0]  # 思源黑体
        self.font = QFont(SourceHanSans)
        self.cap = cv2.VideoCapture(5)
        # phone_num_list, face_data_list = load_encode(seetaFace)

        # self.show_camera_widget = QWidget()
        # self.show_camera_widget.setObjectName('show_camera_widget')
        # self.show_camera_widget.setFixedSize(600, 600)
        # self.show_camera_layout = QGridLayout()
        # self.show_camera_layout.setSpacing(0)
        # self.show_camera_widget.setLayout(self.show_camera_layout)
        # # 设置镜头识别的layout

        # self.show_camera_label = QLabel()
        # self.show_camera_label.setFixedSize(600, 600)
        # self.show_camera_layout.addWidget(self.show_camera_label)

        self.status_bar_widget = QWidget()
        self.status_bar_widget.setObjectName('status_bar_widget')
        self.status_bar_layout = QGridLayout()
        self.status_bar_layout.setSpacing(0)
        self.status_bar_widget.setLayout(self.status_bar_layout)
        self.status_bar_layout.setContentsMargins(0, 0, 10, 0)
        self.status_bar_widget.raise_()
        # 设置顶部状态栏layout

        self.date_widget = QWidget()
        self.date_widget.setObjectName('date_widget')
        self.date_layout = QGridLayout()
        self.date_layout.setSpacing(0)
        self.date_widget.setLayout(self.date_layout)
        self.date_layout.setContentsMargins(0, 0, 0, 0)

        self.date_label = QLabel()
        self.date_label.setObjectName('date_label')
        self.date_label.setFont(self.font)
        self.date_layout.addWidget(self.date_label, 0, 0)
        self.date_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 顶部日期的Label

        self.time_widget = QWidget()
        self.time_widget.setObjectName('time_widget')
        self.time_layout = QGridLayout()
        self.time_layout.setSpacing(0)
        self.time_widget.setLayout(self.time_layout)
        self.time_layout.setContentsMargins(0, 0, 0, 0)

        self.time_label = QLabel()
        self.time_label.setObjectName('time_label')
        self.time_label.setFont(self.font)
        self.time_layout.addWidget(self.time_label, 0, 0, 0, 0)
        self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # 顶部时间的label

        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()
        # 动态显示时间在label上

        self.icon_widget = QWidget()
        self.icon_widget.setObjectName('icon_widget')
        self.icon_layout = QHBoxLayout()
        self.icon_layout.setSpacing(0)
        self.icon_widget.setLayout(self.icon_layout)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_widget.setFixedSize(90, 60)
        # 顶部右侧三个图标定位

        self.signal_widget = QWidget()
        self.signal_widget.setObjectName('signal_widget')
        self.signal_layout = QGridLayout()
        self.signal_layout.setSpacing(0)
        self.signal_widget.setLayout(self.signal_layout)
        self.signal_widget.setFixedSize(23, 23)
        self.signal_layout.setContentsMargins(0, 0, 0, 0)

        self.signal_label = QLabel()
        self.signal_label.setObjectName('signal_label')
        self.signal_layout.addWidget(self.signal_label)
        pix_1 = QPixmap('/home/linaro/Desktop/ui/SVG/svg 2/信号橙.svg')
        self.signal_label.setPixmap(pix_1)
        self.signal_label.setScaledContents(True)
        self.signal_label.setAlignment(QtCore.Qt.AlignLeft)

        self.wifi_widget = QWidget()
        self.wifi_widget.setObjectName('wifi_widget')
        self.wifi_layout = QGridLayout()
        self.wifi_layout.setSpacing(0)
        self.wifi_widget.setLayout(self.wifi_layout)
        self.wifi_widget.setFixedSize(20, 20)
        self.wifi_layout.setContentsMargins(0, 0, 0, 0)

        self.wifi_label = QLabel()
        self.wifi_label.setObjectName('wifi_label')
        self.wifi_layout.addWidget(self.wifi_label)
        pix_2 = QPixmap('/home/linaro/Desktop/ui/SVG/svg 2/WiFi白.svg')
        self.wifi_label.setPixmap(pix_2)
        self.wifi_label.setScaledContents(True)
        self.wifi_label.setAlignment(QtCore.Qt.AlignCenter)

        self.connect_widget = QWidget()
        self.connect_widget.setObjectName('connect_widget')
        self.connect_layout = QGridLayout()
        self.connect_widget.setLayout(self.connect_layout)
        self.connect_widget.setFixedSize(15, 15)
        self.connect_layout.setContentsMargins(0, 0, 0, 0)

        self.connect_label = QLabel()
        self.connect_label.setObjectName('connect_label')
        self.connect_layout.addWidget(self.connect_label)
        pix_3 = QPixmap('/home/linaro/Desktop/ui/SVG/svg 2/接口测试白.svg')
        self.connect_label.setPixmap(pix_3)
        self.connect_label.setScaledContents(True)
        self.connect_label.setAlignment(QtCore.Qt.AlignRight)

        self.icon_layout.addWidget(self.signal_widget)
        self.icon_layout.addWidget(self.wifi_widget)
        self.icon_layout.addWidget(self.connect_widget)

        self.status_bar_layout.addWidget(self.date_widget, 0, 0, 1, 1)
        self.status_bar_layout.addWidget(self.time_widget, 0, 1, 1, 1)
        self.status_bar_layout.addWidget(self.icon_widget, 0, 2, 1, 1)

        self.show_camera_widget = QWidget()
        self.show_camera_widget.setObjectName('show_camera_widget')
        self.show_camera_layout = QGridLayout()
        self.show_camera_layout.setSpacing(0)
        self.show_camera_widget.setLayout(self.show_camera_layout)
        # 设置镜头识别的layout

        self.show_camera_label = QLabel()
        self.show_camera_label.setFixedSize(450, 450)
        # self.show_camera_label.setScaledContents(True)
        self.show_camera_layout.addWidget(self.show_camera_label)

        self.main_layout.addWidget(self.status_bar_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.show_camera_widget, 0, 0, 10, 1)  # 第几行 第几列 占几行 占几列
        QMainWindow.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.setStyleSheet(
            " #status_bar_widget {background-color: rgba(16, 24, 40,0.8)}"
            # " #border {2px solid #FF0000}"
            # " #date_widget{border:2px solid #FF0000}"
            # " #time_widget{border:2px solid #FF0000}"
            # " #icon_widget{border:2px solid #FF0000}"
            # " #signal_widget{border:2px solid #FF0000}"
            # " #connect_widget{border:2px solid #FF0000}"
            # " #wifi_widget{border:2px solid #FF0000}"
            " #date_label {font:15px;color:#FFFFFF;padding-left:10px}"
            " #time_label {font:18px;color:#FFFFFF;font:bold;;padding-left:25px}"
            # " #connect_widget{padding-right:15px}"

        )

    def showtime(self):
        now = QDate.currentDate()
        datetime = QDateTime.currentDateTime()
        text_1 = now.toString("yyyy/MM/dd  dddd")
        text_2 = datetime.toString("h:mm")
        self.date_label.setText(text_1)
        self.time_label.setText(text_2)




class ui_main(QtWidgets.QMainWindow, MainUI):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.initUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = ui_main()
    myWindow.paintEngine()
    myWindow.show()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    sys.exit(app.exec_())
