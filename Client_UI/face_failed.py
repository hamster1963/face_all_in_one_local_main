from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import sys

from PyQt5.uic.properties import QtWidgets


class error_ui(QWidget):
    def __init__(self, parent=None, time=10000, RGB=(16, 24, 40), text='识别失败，请上传人脸信息'):
        super(error_ui, self).__init__(parent)
        self.display_text = text
        self.RGB = RGB
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.action)
        self.timer.start(time)

    def init_ui(self):
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window)  # QtCore.Qt.Window强制该窗口为独立窗口
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.8)  # 设置窗口透明度

        self.main_widget = QWidget(self)
        self.main_widget.setObjectName('main_widget')
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_widget.setLayout(self.main_layout)
        self.main_widget.setFixedSize(480, 133)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.upper_widget = QWidget(self)
        self.upper_widget.setObjectName('upper_widget')
        self.upper_layout = QGridLayout()
        self.upper_layout.setSpacing(0)
        self.upper_widget.setLayout(self.upper_layout)
        self.upper_layout.setContentsMargins(0, 18, 0, 0)

        self.fail_widget = QWidget()
        self.fail_widget.setObjectName('fail_widget')
        self.fail_layout = QGridLayout()
        self.fail_layout.setSpacing(0)
        self.fail_layout.setContentsMargins(0, 0, 0, 0)
        self.fail_widget.setLayout(self.fail_layout)
        self.fail_widget.setFixedSize(48, 48)
        self.fail_label = QLabel()
        self.fail_label.setObjectName('fail_label')
        self.fail_layout.addWidget(self.fail_label)
        pix_1 = QPixmap('/home/linaro/Documents/SVG/错误.svg')
        self.fail_label.setPixmap(pix_1)
        self.fail_label.setScaledContents(True)
        self.fail_label.setAlignment(QtCore.Qt.AlignCenter)

        fontId = QFontDatabase.addApplicationFont(r"/home/linaro/Documents/SourceHanSans.ttf")
        SourceHanSans = QFontDatabase.applicationFontFamilies(fontId)[0]  # 思源黑体
        self.font = QFont(SourceHanSans)

        self.tips_widget = QWidget()
        self.tips_widget.setObjectName('tips_widget')
        # self.tips_widget.setFixedSize(480,60)
        self.tips_layout = QGridLayout()
        self.tips_widget.setLayout(self.tips_layout)
        self.tips_layout.setSpacing(0)
        self.tips_layout.setContentsMargins(0, 0, 0, 0)

        self.tips_label = QLabel('识别失败，请上传人脸信息')
        self.tips_label.setFont(self.font)
        self.tips_label.setObjectName('tips_label')
        self.tips_layout.addWidget(self.tips_label)
        self.tips_label.setAlignment(Qt.AlignCenter)

        self.upper_layout.addWidget(self.fail_widget)
        # self.upper_layout.addWidget(self.line_widget)

        self.main_layout.addWidget(self.upper_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.tips_widget, 1, 0, 1, 1)

        R, G, B, = self.RGB
        self.set_color(R, G, B)

    def set_color(self, R, B, G):
        col = QColor(R, B, G)

        self.setStyleSheet(
            " #main_widget{background-color:#101828}"
            # " #tips_widget{border:2px solid #FF0000}"
            # " #fail_widget{border:2px solid #FF0000}"
            " #tips_label{font-size:22px;color:white;padding-top:0px}"
            " #fail_label{padding-top:2px}"
            # " #line_1_widget{border:2px groove #CCCCCC,;padding-top:15px}"
            # " #line_2_widget{border:1px groove rbg(80,84,94),;padding-top:15px}"
            # " #info_label{font-size:17px;color:#F19D00;regular;opacity:0.5}"
        )

    def action(self):
        self.timer.stop()
        self.hide()


class FaceFailedWidget(error_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setGeometry(100, 305, 480, 360)
        # 居中
        # self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def OPEN(self):
        print('开始显示弹窗')
        # self.setFixedSize(80, 80)
        # app = QApplication(sys.argv)
        self.show()

    def CLOSE(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = FaceFailedWidget()
    ui.OPEN()
    sys.exit(app.exec_())



