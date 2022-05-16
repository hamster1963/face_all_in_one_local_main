import datetime
import sqlite3
import sys
import threading

from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from Client_UI.face_QR import MainUI
from Client_UI.face_success_m_ui import success_ui
from Client_UI.face_failed import error_ui
from seetaface.faceapi import *

# 引擎初始化开始
func_list = ["FACE_RECOGNITION", "LANDMARKER5", "FACE_CLARITY", "FACE_BRIGHT", "FACE_RESOLUTION",
             "FACE_POSE", "FACE_INTEGRITY", "FACE_TRACK"]
model_path = "./seeta/model"
seetaFace = SeetaFace(func_list, device=1, id=0)
seetaFace.SetTrackResolution(640, 480)
seetaFace.init_engine(model_path)
seetaFace.SetInterval(30)
last_PID = ''
frame = ''


# 引擎初始化完毕


def load_encode(seetaFace):
    """
    从数据库中获取保存的手机号与人脸向量
    返还手机号列表以及人脸向量列表
    """
    database = './face.db'
    conn = sqlite3.connect(database)
    # conn.row_factory = sqlite3.Row
    c = conn.cursor()
    phone_num_list = []
    face_data = []
    face_data_list = []
    c.execute('''SELECT staff_id , face_data FROM face_store''')
    conn.commit()
    for row in c:
        phone_num_list.append(row[0])
        face_data.append(row[1])
    for face_data_single in face_data:
        ac = seetaFace.get_feature_by_byte(face_data_single)
        face_data_list.append(ac)
    c.close()
    conn.close()
    print("成功获取到数据库数据")
    return phone_num_list, face_data_list


phone_num_list, face_data_list = load_encode(seetaFace)


class MyWindowClass(QMainWindow, MainUI):
    """
    主窗口类
    """

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        super().__init__(parent)
        self.initUi(self)
        self.setGeometry(100, 0, 480, 640)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.detect_thread = DetectThread()
        self.detect_thread.signal.connect(self.face_result)
        # self.center()

        # self.show_clock = QTimer(self)
        # self.show_clock.timeout.connect(self.fail_show)
        # self.show_clock.start(3000)

        # 显示摄像头线程
        self.time_Display = QTimer(self)  # 处理
        self.time_Display.timeout.connect(self.decodeDisplay)
        self.time_Display.start(30)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def success_show(self):
        """
        成功识别后的界面
        :return:
        """
        show_success = FaceSuccessWidget()
        show_success.OPEN()
        show_success.close_timer = QTimer(show_success)  # 初始化一个定时器
        show_success.close_timer.timeout.connect(show_success.close)  # 计时结束调用operate()方法
        show_success.close_timer.start(2000)  # 设置计时间隔并启动 2s后关闭窗口

    def fail_show(self):
        """
        识别失败后的界面
        :return:
        """
        self.show_fail = FaceFailedWidget()
        self.show_fail.OPEN()
        self.show_fail.close_timer = QTimer(self.show_fail)
        self.show_fail.close_timer.timeout.connect(self.show_fail.close)
        self.show_fail.close_timer.start(2000)  # 设置计时间隔并启动 2s后关闭窗口

    def decodeDisplay(self, ):
        global frame
        self.cap = cv2.VideoCapture(5)  # 初始化摄像头
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (480, 640))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.show_camera_label.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # 转为灰度图像
        self.cap.set(3, 480)
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (640, 480))
        # 人脸画框 #######
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects):
            # print("有人脸")

            for faceRect in faceRects:
                x, y, w, h = faceRect
                # 框选出人脸   最后一个参数2是框线宽度
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # barcodes = pyzbar.decode(gray_image)
        # for barcode in barcodes:
        #     # 提取二维码的位置,然后用边框标识出来在视频中
        #     (x, y, w, h) = barcode.rect
        #     print(x, y, w, h)
        #     X = int((2 * x + w) / 2)
        #     Y = int((2 * y + h) / 2)
        #     cv2.circle(video, (X, Y), 5, (0, 255, 0), 10)
        # 人脸画框 #######
        video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detect_image = QImage(video.data, video.shape[1], video.shape[0],
                              QImage.Format_RGB888)
        self.show_camera_label.setPixmap(QPixmap.fromImage(detect_image))

        # 开始人脸识别线程
        self.detect_thread.start()

        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def face_result(self, msg):
        """
        回调函数，接收人脸识别线程的结果
        :param msg:
        :return:
        """
        if msg == "陌生人":
            print("是陌生人")
            self.fail_show()


class FaceSuccessWidget(success_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 305, 480, 360)
        # 居中
        # self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def OPEN(self):
        # self.setFixedSize(80, 80)
        self.show()

    def CLOSE(self):
        self.close()


class FaceFailedWidget(error_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 505, 480, 133)
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


class DetectThread(QThread):
    """
    人脸识别线程
    """
    signal = pyqtSignal(str)

    def __init__(self):
        super(DetectThread, self).__init__()

    def run(self, ) -> None:
        global frame
        global last_PID
        simage = get_seetaImageData_by_numpy(frame)
        if 1:
            quality_list = []
            detect_result = seetaFace.Track(simage)
            for i in range(detect_result.size):
                face = detect_result.data[i].pos
                PID = detect_result.data[i].PID  # 同一张人脸没有离开视频则其PID 一般不会改变
                if PID == last_PID:
                    pass
                else:
                    points5 = seetaFace.mark5(simage, face)
                    clarity_level = seetaFace.ClarityEvaluate(simage, face, points5)
                    quality_list.append(clarity_level)
                    bright_level = seetaFace.BrightEvaluate(simage, face, points5)
                    quality_list.append(bright_level)

                    # 多种人脸姿态与状态检测 #########
                    resolution_level = seetaFace.ResolutionEvaluate(simage, face, points5)
                    quality_list.append(resolution_level)
                    pose_level = seetaFace.PoseEvaluate(simage, face, points5)
                    quality_list.append(pose_level)
                    integrity_level = seetaFace.IntegrityEvaluate(simage, face, points5)
                    quality_list.append(integrity_level)
                    print(quality_list)
                    # 多种人脸姿态与状态检测 #########

                    if quality_list == ['HIGH', 'HIGH']:
                        # 可以自由设置多种状态检测
                        cal_time_start = datetime.datetime.now()
                        print('开始', cal_time_start)
                        # if 1 == 1:
                        pre = []
                        feature = seetaFace.Extract(simage, points5)
                        for ac in face_data_list:
                            similar1 = seetaFace.CalculateSimilarity(feature, ac)
                            # print('相似度', similar1, phone_num_list[face_data_list.index(ac)])
                            # 相似度大于0.6放入待处理列表中
                            if similar1 >= 0.6:
                                pre.append((phone_num_list[face_data_list.index(ac)], similar1))

                        pre.sort(key=lambda x: x[1], reverse=True)
                        # print('pre', pre)
                        if pre:
                            print(pre[0][0])
                            NAME = pre[0][0]
                            # 发送识别结果
                            self.signal.emit(NAME)
                            last_PID = PID
                        else:
                            print('陌生人')
                            # 发送识别结果
                            self.signal.emit("陌生人")
                            last_PID = PID
                            cal_time_end = datetime.datetime.now()
                            print('结束', cal_time_end)
                            print(cal_time_end - cal_time_start)


def ui_show():
    """
    UI显示
    :return:
    """
    global app
    try:
        app = QtWidgets.QApplication(sys.argv)
        myWindow = MyWindowClass()
        myWindow.paintEngine()
        myWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        print(e.__traceback__.tb_lineno)


if __name__ == '__main__':
    ui_show()
    th = threading.Thread(target=ui_show)  # 创建一个线程
    th.start()  # 启动线程
