import multiprocessing as mp

from seetaface.faceapi import *
import sqlite3

import cv2
import datetime
import sys

last_PID = ''
NAME = ''



# 引擎初始化
def load_encode(seetaFace):
    """
    从数据库中获取保存的手机号与人脸向量
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


def image_put(q):

    # 引擎初始化
    func_list = ["FACE_RECOGNITION", "LANDMARKER5", "FACE_CLARITY", "FACE_BRIGHT", "FACE_RESOLUTION",
                 "FACE_POSE", "FACE_INTEGRITY", "FACE_TRACK"]
    model_path = "./seeta/model"
    seetaFace = SeetaFace(func_list, device=1, id=0)
    seetaFace.SetTrackResolution(640, 480)
    seetaFace.init_engine(model_path)
    seetaFace.SetInterval(30)
    cap = cv2.VideoCapture(5)
    flag, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    if cap.isOpened():
        print('摄像头开启')
    else:
        print('DaHua')
    while True:
        q.put(cap.read()[1])
        # q.get() if q.qsize() > 1 else time.sleep(0.01)
        faceImg = cap.read()[1]  # 读取摄像头图像
        gray = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
        classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faceRects = classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects):
            for faceRect in faceRects:
                x, y, w, h = faceRect
                # 框选出人脸   最后一个参数2是框线宽度
                cv2.rectangle(faceImg, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("track", faceImg)
        # ui_show(cap.read()[1])


        k = cv2.waitKey(10)  # 键盘值
        if k == 27:  # 通过esc键退出摄像
            break


def image_test(q, ):
    # 引擎初始化
    func_list = ["FACE_RECOGNITION", "LANDMARKER5", "FACE_CLARITY", "FACE_BRIGHT", "FACE_RESOLUTION",
                 "FACE_POSE", "FACE_INTEGRITY", "FACE_TRACK"]
    model_path = "./seeta/model"
    seetaFace = SeetaFace(func_list, device=1, id=0)
    seetaFace.SetTrackResolution(640, 480)
    seetaFace.init_engine(model_path)
    seetaFace.SetInterval(30)

    last_PID = ''
    # 初始化数据库
    phone_num_list, face_data_list = load_encode(seetaFace)

    global NAME
    while True:
        frame = q.get()
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
                    # resolution_level = seetaFace.ResolutionEvaluate(simage, face, points5)
                    # quality_list.append(resolution_level)
                    # pose_level = seetaFace.PoseEvaluate(simage, face, points5)
                    # quality_list.append(pose_level)
                    # integrity_level = seetaFace.IntegrityEvaluate(simage, face, points5)
                    # quality_list.append(integrity_level)
                    # print(quality_list)
                    if quality_list == ['HIGH', 'HIGH']:
                        cal_time_start = datetime.datetime.now()
                        print('开始', cal_time_start)
                        # if 1 == 1:
                        pre = []
                        feature = seetaFace.Extract(simage, points5)
                        for ac in face_data_list:
                            similar1 = seetaFace.CalculateSimilarity(feature, ac)
                            # print('相似度', similar1, phone_num_list[face_data_list.index(ac)])
                            if similar1 >= 0.6:
                                pre.append((phone_num_list[face_data_list.index(ac)], similar1))

                        pre.sort(key=lambda x: x[1], reverse=True)
                        # print('pre', pre)
                        if pre:
                            print(pre[0][0])
                            NAME = pre[0][0]
                            last_PID = PID
                        else:
                            print('陌生人')
                            last_PID = PID
                            cal_time_end = datetime.datetime.now()
                            print('结束', cal_time_end)
                            print(cal_time_end - cal_time_start)
        # frame = cv2.resize(cap.read()[1], (640, 480))
        # cv2.imshow('window_name', frame)
        # cv2.waitKey(1)


def run_single_camera():
    global processes
    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=3)
    # processes = [mp.Process(target=image_put, args=(queue,)),
    #              mp.Process(target=image_get, args=(queue,)),
    #              mp.Process(target=image_test, args=(queue,)), ]
    processes = [  # mp.Process(target=ui_show, args=(queue,)),
        mp.Process(target=image_put, args=(queue,)),
        mp.Process(target=image_test, args=(queue,)),
    ]
    try:
        for process in processes:
            process.daemon = True
            process.start()
        [process.join() for process in processes]
    except KeyboardInterrupt:
        print("mian stop...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        sys.exit(1)




def run():
    run_single_camera()
if __name__ == '__main__':
    run()
