from PyQt5.QtCore import QSize, QTimer, Qt, QRect
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class ico_label(QLabel):
    def __init__(self, *args, antialiasing=True, pix_path=" ", **kwargs):
        super(ico_label, self).__init__(*args, **kwargs, )
        self.Antialiasing = antialiasing
        self.setFixedSize(80, 80)
        # self.setMinimumSize(75, 75)
        self.radius = 100
        self.pix = pix_path
        #####################核心实现#########################
        self.target = QPixmap(self.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明
        p = QPixmap(self.pix).scaled(  # 加载图片并缩放和控件一样大
            80, 80, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter = QPainter(self.target)
        if self.Antialiasing:
            # 抗锯齿
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
            #         painter.setPen(# 测试黑色圆圈
            #             QPen(Qt.black, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            pen = QPen(QColor('#f19d00'))  # 设置边框颜色
            pen.setWidth(5)  # 设置边框宽度
            painter.setPen(pen)  # 添加描边边框
            rect = QRect(2, 2, self.width() - 5, self.height() - 5)  # 构造一个以（x，y）为左上角、给定宽度和高度的矩形。
            painter.drawRoundedRect(rect, self.width() / 2, self.height() / 2)
        path = QPainterPath()
        path.addRoundedRect(
            2, 2, self.width() - 5, self.height() - 5, self.radius, self.radius)  # 要与上面rect保持一致
        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        #         painter.drawPath(path)  # 测试黑色圆圈
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)


class success_ui(QWidget):
    def __init__(self, parent=None, time=500000, RGB=(16, 24, 40)):
        super(success_ui, self).__init__(parent)
        self.RGB = RGB
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.action)
        self.timer.start(time)

    def init_ui(self):
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window)  # QtCore.Qt.Window强制该窗口为独立窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)  # 设置窗口透明度

        fontId = QFontDatabase.addApplicationFont(r"/home/linaro/Desktop/ui/SourceHanSans.ttf")
        SourceHanSans = QFontDatabase.applicationFontFamilies(fontId)[0]  # 思源黑体
        self.font = QFont(SourceHanSans)

        self.main_widget = QWidget(self)
        self.main_widget.setObjectName('main_widget')
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setFixedSize(480, 360)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.upper_widget = QWidget(self)
        self.upper_widget.setObjectName('upper_widget')
        self.upper_layout = QGridLayout()
        self.upper_layout.setSpacing(0)
        self.upper_widget.setLayout(self.upper_layout)
        self.upper_widget.setFixedSize(480, 103)
        self.upper_layout.setContentsMargins(0, 0, 0, 0)
        # 顶部大框架

        self.blank_widget = QWidget(self)
        self.blank_widget.setObjectName("blank_widget")
        self.blank_layout = QGridLayout()
        self.blank_layout.setSpacing(0)
        self.blank_widget.setLayout(self.blank_layout)
        self.blank_layout.setContentsMargins(0, 0, 0, 0)
        self.blank_label = QLabel()
        self.blank_layout.addWidget(self.blank_label)
        # 顶部框架分两行——1

        self.blank_1_widget = QWidget(self)
        self.blank_1_widget.setObjectName("blank_1_widget")
        self.blank_1_layout = QGridLayout()
        self.blank_1_layout.setSpacing(0)
        self.blank_1_widget.setLayout(self.blank_1_layout)
        self.blank_1_layout.setContentsMargins(0, 0, 0, 0)
        # 顶部框架分两行——2

        self.upper_layout.addWidget(self.blank_widget, 0, 0, 1, 1)
        self.upper_layout.addWidget(self.blank_1_widget, 1, 0, 1, 1)

        self.ico_widget = QWidget()
        self.ico_widget.setObjectName("ico_widget")
        self.ico_layout = QGridLayout()
        self.ico_layout.setSpacing(0)
        self.ico_widget.setLayout(self.ico_layout)
        self.ico_widget.setFixedSize(120, 120)
        self.ico_layout.setContentsMargins(20, 5, 10, 10)  # 左上右下 20,10,10,0

        self.ico_label = QLabel()
        self.ico_label.setObjectName("ico_label")
        self.ico_label.setFixedSize(90, 90)
        self.ico_layout.addWidget(self.ico_label)
        self.ico_label.setScaledContents(True)
        self.ico_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ico_layout.addWidget(ico_label(self, pix_path='234.jpeg'))

        # 头像部分区域

        self.profile_Widget = QWidget(self)
        self.profile_Widget.setObjectName('profile_widget')
        self.profile_layout = QGridLayout()
        self.profile_Widget.setLayout(self.profile_layout)
        self.profile_Widget.setFixedSize(480, 103)

        # 圆形头像

        self.blank_2_label = QLabel()
        self.blank_3_label = QLabel()

        self.profile_layout.addWidget(self.ico_label, 0, 0, 4, 2)
        self.profile_layout.addWidget(self.blank_2_label, 0, 2, 4, 6)
        self.profile_layout.addWidget(self.blank_3_label, 1, 2, 4, 6)

        self.top_widget = QWidget(self)
        self.top_widget.setObjectName('top_widget')
        self.top_layout = QGridLayout()
        self.top_layout.setSpacing(0)
        self.top_widget.setLayout(self.top_layout)
        self.top_widget.setFixedSize(600, 52)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.blank_1_layout.addWidget(self.top_widget)
        # 顶部信息栏大框

        self.icon_widget = QWidget()
        self.icon_widget.setObjectName('icon_widget')
        self.icon_layout = QHBoxLayout()
        self.icon_layout.setSpacing(0)
        self.icon_widget.setLayout(self.icon_layout)
        self.icon_layout.setContentsMargins(0, 0, 0, 10)  # 左上右下
        self.icon_widget.setFixedSize(360, 52)

        self.member_widget = QWidget()
        self.member_widget.setObjectName('member_widget')
        self.member_layout = QGridLayout()
        self.member_layout.setSpacing(0)
        self.member_widget.setLayout(self.member_layout)
        self.member_widget.setFixedSize(20, 20)
        self.member_layout.setContentsMargins(0, 0, 0, 0)

        self.member_label = QLabel()
        self.member_label.setObjectName('member_label')
        self.member_layout.addWidget(self.member_label)
        pix_1 = QPixmap('/Users/liaolaixin/Desktop/人脸一体机/消费机UI界面/SVG/新建文件夹/人员.svg')
        self.member_label.setPixmap(pix_1)
        self.member_label.setScaledContents(True)
        self.member_label.setAlignment(QtCore.Qt.AlignLeft)

        self.member_1_label = QLabel("司徒相如")
        self.member_1_label.setObjectName('m_1_label')
        self.member_1_label.setFont(self.font)
        self.member_1_label.setFixedSize(80, 40)

        self.section_widget = QWidget()
        self.section_widget.setObjectName('section_widget')
        self.section_layout = QGridLayout()
        self.section_layout.setSpacing(0)
        self.section_widget.setLayout(self.section_layout)
        self.section_widget.setFixedSize(25, 23)
        self.section_layout.setContentsMargins(0, 0, 0, 0)

        self.section_label = QLabel()
        self.section_label.setObjectName('section_label')
        self.section_layout.addWidget(self.section_label)
        pix_2 = QPixmap('/Users/liaolaixin/Desktop/人脸一体机/消费机UI界面/SVG/新建文件夹/通讯录.svg')
        self.section_label.setPixmap(pix_2)
        self.section_label.setScaledContents(True)
        self.section_label.setAlignment(QtCore.Qt.AlignCenter)

        self.section_1_label = QLabel("五邑大学经济管...")
        self.section_1_label.setObjectName("m_1_label")
        self.section_1_label.setFixedSize(130, 40)
        self.section_1_label.setFont(self.font)

        self.meal_widget = QWidget()
        self.meal_widget.setObjectName('meal_widget')
        self.meal_layout = QGridLayout()
        self.meal_layout.setSpacing(0)
        self.meal_widget.setLayout(self.meal_layout)
        self.meal_widget.setFixedSize(20, 20)
        self.meal_layout.setContentsMargins(0, 0, 0, 0)

        self.meal_label = QLabel()
        self.meal_label.setObjectName('meal_label')
        self.meal_layout.addWidget(self.meal_label)
        pix_3 = QPixmap('/Users/liaolaixin/Desktop/人脸一体机/消费机UI界面/SVG/新建文件夹/时间.svg')
        self.meal_label.setPixmap(pix_3)
        self.meal_label.setScaledContents(True)
        self.meal_label.setAlignment(QtCore.Qt.AlignRight)

        self.meal_1_label = QLabel("午餐")
        self.meal_1_label.setObjectName("m_1_label")
        self.meal_1_label.setFont(self.font)
        self.meal_1_label.setFixedSize(70, 40)

        self.icon_layout.addWidget(self.member_widget)
        self.icon_layout.addWidget(self.member_1_label)
        self.icon_layout.addWidget(self.section_widget)
        self.icon_layout.addWidget(self.section_1_label)
        self.icon_layout.addWidget(self.meal_widget)
        self.icon_layout.addWidget(self.meal_1_label)

        self.top_layout.addWidget(self.icon_widget, 1, 3, 1, 6)
        # 顶部图标布局

        self.upper_layout.addWidget(self.ico_widget, 0, 0, 0, 2)
        self.upper_layout.addWidget(self.top_widget, 1, 2, 1, 1)

        self.center_widget = QWidget(self)
        self.center_widget.setObjectName('center_widget')
        self.center_layout = QGridLayout()
        self.center_layout.setSpacing(0)
        self.center_widget.setLayout(self.center_layout)
        self.center_widget.setFixedSize(480, 125)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        # 图标大框

        self.u1_widget = QWidget()
        self.u1_widget.setObjectName('u1_widget')
        self.u1_layout = QHBoxLayout()
        self.u1_layout.setSpacing(0)
        self.u1_widget.setLayout(self.u1_layout)
        self.u1_layout.setContentsMargins(0, 0, 0, 0)
        self.u1_widget.setFixedSize(400, 70)

        self.pix_widget = QWidget()
        self.pix_widget.setObjectName('pix_widget')
        self.pix_layout = QGridLayout()
        self.pix_layout.setSpacing(0)
        self.pix_layout.setContentsMargins(0, 0, 0, 0)
        self.pix_widget.setLayout(self.pix_layout)
        self.pix_widget.setFixedSize(48, 48)
        self.pix_label = QLabel()
        self.pix_label.setObjectName('pix_label')
        self.pix_layout.addWidget(self.pix_label)
        pix_4 = QPixmap('/Users/liaolaixin/Desktop/人脸一体机/消费机UI界面/SVG/确认 圆 正确 对勾 提交 成功 完成  (1).svg')
        self.pix_label.setPixmap(pix_4)
        self.pix_label.setScaledContents(True)
        self.pix_label.setAlignment(Qt.AlignCenter)

        self.u1_layout.addWidget(self.pix_widget)
        # 中间部分图标

        self.u2_widget = QWidget()
        self.u2_widget.setObjectName('u2_widget')
        self.u2_layout = QHBoxLayout()
        self.u2_layout.setSpacing(0)
        self.u2_widget.setLayout(self.u2_layout)
        self.u2_layout.setContentsMargins(0, 0, 0, 0)
        self.u2_widget.setFixedSize(400, 55)

        self.tips_widget = QWidget()
        self.tips_widget.setObjectName('tips_widget')
        self.tips_layout = QGridLayout()
        self.tips_widget.setLayout(self.tips_layout)
        self.tips_layout.setSpacing(0)
        self.tips_widget.setFixedSize(150, 30)
        self.tips_layout.setContentsMargins(0, 0, 0, 0)

        self.tips_label = QLabel('第2份扣费成功')
        self.tips_label.setFont(self.font)
        self.tips_label.setObjectName('tips_label')
        self.tips_layout.addWidget(self.tips_label)
        self.tips_label.setScaledContents(True)
        self.tips_label.setAlignment(Qt.AlignCenter)

        self.u2_layout.addWidget(self.tips_widget)
        # 中间部分提示语

        self.center_layout.addWidget(self.u1_widget, 0, 0, 1, 0)
        self.center_layout.addWidget(self.u2_widget, 1, 0, 1, 0)
        # 中间图标+提示语布局

        self.u3_widget = QWidget()
        self.u3_widget.setObjectName('u3_widget')
        self.u3_layout = QHBoxLayout()
        self.u3_layout.setSpacing(0)
        self.u3_widget.setLayout(self.u3_layout)
        self.u3_layout.setContentsMargins(0, 0, 0, 0)
        self.u3_widget.setFixedSize(480, 2)

        self.groove_widget = QWidget()
        self.groove_widget.setObjectName('groove_widget')
        self.groove_layout = QGridLayout()
        self.groove_layout.setSpacing(0)
        self.groove_widget.setLayout(self.groove_layout)
        self.groove_widget.setFixedSize(400, 2)  # groove_widget 设成400*2

        self.groove_label = QLabel()
        self.groove_label.setObjectName('groove_label')
        self.groove_layout.addWidget(self.groove_label)
        self.groove_label.setScaledContents(True)
        self.groove_label.setAlignment(Qt.AlignCenter)

        self.u3_layout.addWidget(self.groove_widget)
        # 分割线(居中位置）

        self.bottom_widget = QWidget(self)
        self.bottom_widget.setObjectName('bottom_widget')
        self.bottom_layout = QGridLayout()
        self.bottom_layout.setSpacing(0)
        self.bottom_widget.setLayout(self.bottom_layout)
        self.bottom_widget.setFixedSize(480, 160)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        # 底部内容框

        self.bottom2_widget = QWidget(self)
        self.bottom2_widget.setObjectName('bottom2_widget')
        self.bottom2_layout = QGridLayout()
        self.bottom2_layout.setSpacing(0)
        self.bottom2_widget.setLayout(self.bottom2_layout)
        self.bottom2_widget.setFixedSize(440, 140)
        self.bottom2_layout.setContentsMargins(0, 0, 0, 0)

        self.price_label = QLabel("定价")
        self.price_label.setObjectName("bottomfix")
        self.price_label.setFont(self.font)
        self.label_1 = QLabel("56.00")
        self.label_1.setObjectName("label_")
        self.label_1.setFont(self.font)
        self.label_1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.copies_label = QLabel("份数")
        self.copies_label.setObjectName("bottomfix")
        self.copies_label.setFont(self.font)
        self.label_2 = QLabel("4")
        self.label_2.setObjectName("label_")
        self.label_2.setFont(self.font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.fee_label = QLabel("扣费")
        self.fee_label.setObjectName("bottomfix")
        self.fee_label.setFont(self.font)
        self.label_3 = QLabel()
        self.label_3.setObjectName("label_")
        self.label_3.setFont(self.font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.balance_label = QLabel("余额")
        self.balance_label.setObjectName("bottomfix")
        self.balance_label.setFont(self.font)
        self.label_4 = QLabel("#60.00")
        self.label_4.setObjectName("label_")
        self.label_4.setFont(self.font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.menu_label = QLabel('奥尔良鸡翅\n鸡扒饭')
        self.menu_label.setObjectName("menu")
        self.menu_label.setFont(self.font)
        self.menu_label.setAlignment(QtCore.Qt.AlignRight)

        def info_(menu, num):
            if len(menu) >= 7:
                print(str(menu[0:2]) + "···" + str(menu[-3:]) + "\t" + str(num) + "\n")
            else:
                print(menu, num)
            self.menu_label.setText(info_())

        self.bottom2_layout.addWidget(self.price_label, 0, 0, 1, 1)
        self.bottom2_layout.addWidget(self.label_1, 0, 1, 1, 1)
        self.bottom2_layout.addWidget(self.copies_label, 1, 0, 1, 1)
        self.bottom2_layout.addWidget(self.label_2, 1, 1, 1, 1)
        self.bottom2_layout.addWidget(self.fee_label, 2, 0, 1, 1)
        self.bottom2_layout.addWidget(self.label_3, 2, 1, 1, 1)
        self.bottom2_layout.addWidget(self.balance_label, 3, 0, 1, 1)
        self.bottom2_layout.addWidget(self.label_4, 3, 1, 1, 1)
        self.bottom2_layout.addWidget(self.menu_label, 0, 2, 6, 2)
        self.bottom_layout.addWidget(self.bottom2_widget)
        # 底部布局

        self.main_layout.addWidget(self.profile_Widget, 0, 0, 2, 3)
        self.main_layout.addWidget(self.upper_widget, 0, 0, 2, 8)
        self.main_layout.addWidget(self.top_widget, 1, 2, 0, 6)
        self.main_layout.addWidget(self.center_widget, 3, 0, 1, 7)
        self.main_layout.addWidget(self.u3_widget, 4, 0, 1, 7)
        self.main_layout.addWidget(self.bottom_widget, 5, 0, 1, 7)
        # 主窗口布局

        R, G, B, = self.RGB
        self.set_color(R, G, B)

    def set_color(self, R, B, G):
        col = QColor(R, B, G)

        self.setStyleSheet(
            " #blank_1_widget{background-color:#101828}"
            " #icon_widget{background-color:#101828}"
            " #m_1_label{color:white;padding-left:3px}"
            " #tips_widget{background-color:#101828}"
            " #center_widget{background-color:#101828}"
            " #groove_widget {border:2px groove #242833}"  # CCCCCC  808A87 323847 313645 222630 23262f  16181f 181a20 #242833
            " #u3_widget{background-color:#101828}"
            " #bottom_widget{background-color:#101828}"
            " #bottom2_widget{background-color:#101828}"
            " #tips_label{font-size:22px;color:white;padding-top:0px}"
            " #bottomfix{font-size:15px;color:white;padding-left:15px}"
            " #label_{color:#F19D00;font-size:15px;Bold;padding-right:15px}"
            " #menu{padding-right:15px;font-size:15px;color:white}"

            # " #main_widget{background-color:#CCCCCC}"
            # " #upper_widget{border:2px solid #FF0000}"
            # " #blank_widget{border:2px solid #FF0000}"
            # " #blank_2{border:2px solid #FF0000}"
            # " #ico_widget{border:2px solid #FF0000}"
            # " #profile_widget{border:2px solid #FF0000}"
            # " #ico_label{order:2px solid #FF0000}"
            # " #top_widget{border:2px solid #CCCCCC}"
            # " #icon_widget{border:2px solid #FF0000}"
            # " #m_1_label{border:2px solid #CCCCCC}"
            # " #m_1_label{color:white;padding-left:3px}"
            # " #tips_widget{border:2px solid #FF0000}"
            # " #pix_widget{border:2px solid #FF0000}"
            # " #center_widget{border:2px solid #FF0000}"
            # " #u3_widget{border:2px solid #FF0000}"
            # " #groove_widget {border:2px groove #242833}"#  CCCCCC  808A87 323847 313645 222630 23262f  16181f 181a20 #242833
            # " #bottom_widget{border:2px solid #FF0000}"
            # " #bottom2_widget{border:2px solid #FF0000}"
            # " #tips_label{font-size:22px;color:white;padding-top:0px}"
            # " #pix_label{padding-top:0px}"
            # " #bottomfix{font-size:15px;color:white;padding-left:15px}"
            # " #label_{color:#F19D00;font-size:15px;Bold;padding-right:15px}"
            # " #menu{color:#FFFFFF;border:2px solid #CCCCCC}"

        )

    def action(self):
        self.timer.stop()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = success_ui()
    ui.show()
    sys.exit(app.exec_())
