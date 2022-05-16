from seetaface.faceapi import *
import sqlite3
import datetime
import cv2

# 引擎初始化
func_list = ["FACE_DETECT", "FACE_RECOGNITION", "LANDMARKER5", "FACE_CLARITY", "FACE_BRIGHT", "FACE_RESOLUTION",
             "FACE_POSE", "FACE_INTEGRITY", "FACE_TRACK"]
model_path = "./seeta/model"
seetaFace = SeetaFace(func_list, device=1, id=0)
seetaFace.SetTrackResolution(310, 310)
seetaFace.init_engine(model_path)
phone_num_list = []
face_data_list = []


def load_encoding():
    """
    从数据库中获取保存的手机号与人脸向量
    """
    database = './face.db'
    conn = sqlite3.connect(database)
    # conn.row_factory = sqlite3.Row
    c = conn.cursor()
    phone_num = []
    face_data = []
    c.execute('''SELECT staff_id , face_data FROM face_store''')
    conn.commit()
    for row in c:
        phone_num.append(row[0])
        face_data.append(row[1])
    facedata_list = []
    for face_data_single in face_data:
        ac = seetaFace.get_feature_by_byte(face_data_single)
        facedata_list.append(ac)
    c.close()
    conn.close()
    return phone_num, facedata_list


def face_system_init():
    """
    读取人脸数据库
    :return:
    """
    global phone_num_list
    global face_data_list
    try:
        phone_num, face_data_list = load_encoding()
    except Exception as e:
        print(e)
        print("数据库读取失败")
    else:
        print('人脸数据库读取成功')


def face_score(img_url, score_threshold=0.8):
    """
    人脸照片分数评估
    :param img_url:
    :param score_threshold:
    :return:
    """
    image = cv2.imread(img_url)  # 原图
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 人脸检测
    detect_result = seetaFace.Detect(simage)
    raw_data = detect_result.data
    face_num = detect_result.size
    # 如果检测到一张人脸
    if face_num == 1:
        score = raw_data[0].score
        # 大于人脸分数阈值
        if score > score_threshold:
            return score
        else:
            return False
    else:
        return False


def frame_quality():
    """
    检测该帧图像是够符合要求
    :return:
    """
    camera = cv2.VideoCapture(5)
    if camera.isOpened():
        while 1:
            flag, frame = camera.read()
            if flag:
                simage = get_seetaImageData_by_numpy(frame)
                detectr_result = seetaFace.Track(simage)
                for i in range(detectr_result.size):
                    # 人脸位置
                    face = detectr_result.data[i].pos
                    # 人脸编号
                    PID = detectr_result.data[i].PID
                    cv2.rectangle(frame, (face.x, face.y), (face.x + face.width, face.y + face.height), (255, 0, 0), 2)
                    cv2.putText(frame, "pid:{}".format(PID), (face.x, face.y), 1, 1, (0, 0, 255))
                cv2.imshow("track", frame)
                cv2.waitKey(30)


# frame_quality()
'''
print('start')
image = cv2.imread("./images/me.jpg")  # 原图
simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
# 人脸检测
detect_result = seetaFace.Detect(simage)
rect_list = detect_result.data
print("result", detect_result)
face1 = detect_result.data[0].pos
# 特征点检测
points5 = seetaFace.mark5(simage, face1)  # 5特征点检测
# 清晰度
clarity_level = seetaFace.ClarityEvaluate(simage, face1, points5)
print("清晰度质量:", clarity_level)
# 明亮度
bright_level = seetaFace.BrightEvaluate(simage, face1, points5)
print("明亮度质量:", bright_level)
# 分辨率质量
resolution_level = seetaFace.ClarityEvaluate(simage, face1, points5)
print("分辨率质量:", resolution_level)
# 人脸姿态角质量
pose_level = seetaFace.BrightEvaluate(simage, face1, points5)
print("人脸姿态角质量:", pose_level)
# 人脸完整性质量
integrity_level = seetaFace.BrightEvaluate(simage, face1, points5)
print("人脸完整性质量:", integrity_level)'''


def crop_extract(img_url):
    """
    裁剪并获取特征值
    :param img_url:
    :return:
    """
    image = cv2.imread(img_url)  # 原图
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 进行人脸检测
    detect_result2 = seetaFace.Detect(simage)
    face_num = detect_result2.size
    # 如果检测到一张人脸
    if face_num == 1:
        face2 = detect_result2.data[0].pos
        points = seetaFace.mark5(simage, face2)
        feature = seetaFace.Extract(simage, points)
        return feature
    else:
        return 'face_false'


def SQL_DML_SEL(db_path, dml_sel, params=None):
    """
    sql 查询语句
    :param params:
    :param db_path: 数据库路径
    :param dml_sel: SQL查询
    :return:sel_result: 查询结果
    """
    if params is None:
        params = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(dml_sel, params)
    sel_result = cursor.fetchall()
    cursor.close()
    conn.commit()  # 提交事务
    conn.close()  # 关闭Connection
    return sel_result


def SQL_DML_UPD(db_path, dml_upd, params=None):
    """
    sql 查询语句
    :param params:
    :param db_path: 数据库路径
    :param dml_upd: SQL更新
    :return:查询结果
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(dml_upd, params)
    cursor.close()
    conn.commit()  # 提交事务
    conn.close()  # 关闭Connection


def SQL_DML_INS(db_path, dml_ins, params=None):
    """
    sql 查询语句
    :param params:
    :param db_path: 数据库路径
    :param dml_ins: SQL插入
    :return:查询结果
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(dml_ins, params)
    cursor.close()
    conn.commit()  # 提交事务
    conn.close()  # 关闭Connection


def create_store(name, face_data, company_id, staff_id, phone_num, update_time):
    """
    向数据库注册人脸
    """
    database = './face.db'
    search_name = "SELECT COUNT(*) FROM face_store WHERE staff_id = ?"
    staff_state = SQL_DML_SEL(database, search_name, [staff_id])[0][0]
    # 判断是否已存在该用户信息，已经存在则update
    if staff_state != 0:
        try:
            update_face_data = "UPDATE face_store SET face_data = ? WHERE staff_id = ?"
            SQL_DML_UPD(database, update_face_data, [face_data, staff_id])
        except Exception as e:
            print(e)
        else:
            update_encode_state = "UPDATE face_store SET encode_state = 1 WHERE staff_id= ?"
            SQL_DML_UPD(database, update_encode_state, [staff_id])
            print("人脸id:%s数据更新成功" % name)
    else:
        try:
            insert_face_data = "INSERT INTO face_store (name, face_data, company_id, staff_id, phone_num, update_time) VALUES (?,?,?,?,?,?)"
            SQL_DML_INS(database, insert_face_data, [name, face_data, company_id, staff_id, phone_num, update_time])
        except Exception as e:
            print(e)
        else:
            update_encode_state = "UPDATE face_store SET encode_state = 1 WHERE staff_id= ?"
            SQL_DML_UPD(database, update_encode_state, [staff_id])
            print("人脸id:%s数据插入成功" % name)


'''def main():
    """
    人脸比对主函数
    :return:
    """
    print('start', time.time())
    pre = []
    for ac in face_data_list:
        similar1 = seetaFace.CalculateSimilarity(a, ac)
        print('相似度', similar1, phone_list[face_data_list.index(ac)])
        if similar1 >= 0.6:
            pre.append((phone_list[face_data_list.index(ac)], similar1))
    print(pre)
    pre.sort(key=lambda x: x[1], reverse=True)
    print(pre[0][0])
    print('start', time.time())

main()'''


# 批量文件夹注册人脸
def get_file_list(dir):
    file_list = []
    file_num = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_type = str(file).split('.')[1]
            # 判断文件类型
            if file_type in ['jpg', 'png', 'jpeg']:
                file_list.append(os.path.join(root, file))
                file_num.append(str(file).split('.')[0])

    staff_id = 0
    false_list = []
    success_list = []
    for url in file_list:
        staff_id += 1
        company_id = 999
        phone_num = file_num[file_list.index(url)]
        face_data = crop_extract(url)
        # 获取到a的二进制特征值
        if face_data != 'face_false':
            try:
                data = seetaFace.get_feature_byte(face_data)
                name = file_num[file_list.index(url)]
                update_time = datetime.datetime.now()
                print('name是', name)
                create_store(name, data, company_id, staff_id, phone_num, update_time)
            except Exception as e:
                print(e)
                false_list.append(url)
            else:
                success_list.append(url)
        else:
            false_list.append(url)
    print('false_list', false_list)
    print('success_list', success_list)


def sql_test():
    staff_id = 16
    database = './face.db'
    search_name = "SELECT COUNT(*) FROM face_store WHERE staff_id = ?"
    staff_state = SQL_DML_SEL(db_path=database, dml_sel=search_name, params=[staff_id])[0][0]
    print(staff_state)

sql_test()