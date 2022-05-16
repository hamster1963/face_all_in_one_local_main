import threading
from copy import deepcopy
from seetaface.faceapi import *
import sqlite3

# 引擎初始化
func_list = ["FACE_DETECT", "FACE_RECOGNITION", "LANDMARKER5", "FACE_CLARITY", "FACE_BRIGHT", "FACE_RESOLUTION",
             "FACE_POSE", "FACE_INTEGRITY", "FACE_TRACK"]
model_path = "./seeta/model"
seetaFace = SeetaFace(func_list, device=1, id=0)
seetaFace.SetTrackResolution(640, 480)


seetaFace.init_engine(model_path)
phone_num_list = []
face_data_list = []

seetaFace.SetInterval(30)
seetaFace.SetSingleCalculationThreads(4)

def load_encoding():
    """
    从数据库中获取保存的手机号与人脸向量
    """
    global phone_num_list
    global face_data_list
    database = './face.db'
    conn = sqlite3.connect(database)
    # conn.row_factory = sqlite3.Row
    c = conn.cursor()
    phone_num_list = []
    face_data = []
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


load_encoding()


thread_lock = threading.Lock()
thread_exit = False

class myThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):
        global thread_exit
        cap = cv2.VideoCapture(self.camera_id)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        while not thread_exit:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (self.img_width, self.img_height))
                thread_lock.acquire()
                self.frame = frame
                thread_lock.release()
            else:
                thread_exit = True
        cap.release()

def main():
    global thread_exit
    last_PID = ''
    camera_id = 5
    img_height = 480
    img_width = 640
    thread = myThread(camera_id, img_height, img_width)
    thread.start()

    while not thread_exit:
        thread_lock.acquire()
        frame = thread.get_frame()
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
                    pass
                    points5 = seetaFace.mark5(simage, face)
                    clarity_level = seetaFace.ClarityEvaluate(simage, face, points5)
                    quality_list.append(clarity_level)
                    bright_level = seetaFace.BrightEvaluate(simage, face, points5)
                    quality_list.append(bright_level)
                    resolution_level = seetaFace.ClarityEvaluate(simage, face, points5)
                    quality_list.append(resolution_level)
                    pose_level = seetaFace.BrightEvaluate(simage, face, points5)
                    quality_list.append(pose_level)
                    integrity_level = seetaFace.BrightEvaluate(simage, face, points5)
                    quality_list.append(integrity_level)
                    # print(quality_list)
                    if quality_list == ['HIGH', 'HIGH', 'HIGH', 'HIGH', 'HIGH']:
                        pre = []
                        feature = seetaFace.Extract(simage, points5)
                        for ac in face_data_list:
                            similar1 = seetaFace.CalculateSimilarity(feature, ac)
                            # print('相似度', similar1, phone_num_list[face_data_list.index(ac)])
                            if similar1 >= 0.6:
                                pre.append((phone_num_list[face_data_list.index(ac)], similar1))
                        pre.sort(key=lambda x: x[1], reverse=True)
                        if pre:
                            print(pre[0][0])
                            last_PID = PID

                cv2.rectangle(frame, (face.x, face.y), (face.x + face.width, face.y + face.height), (255, 0, 0), 2)
                cv2.putText(frame, "pid:{}".format(PID), (face.x, face.y), 1, 1, (0, 0, 255))
        thread_lock.release()

        cv2.imshow('Video', frame)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            thread_exit = True
    thread.join()

if __name__ == "__main__":
    main()

