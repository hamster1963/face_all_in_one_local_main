from seetaface.faceapi import *

# 引擎初始化
func_list = ["FACE_DETECT", "FACE_RECOGNITION", "LANDMARKER5", "FACE_CLARITY", "FACE_BRIGHT", "FACE_RESOLUTION",
             "FACE_POSE", "FACE_INTEGRITY", ]
model_path = "./seeta/model"
seetaFace = SeetaFace(func_list, device=1, id=0)
seetaFace.SetTrackResolution(310, 310)
seetaFace.init_engine(model_path)

import numpy as np
import cv2
from PIL import Image


def pose_predict(image):
    """
    人脸姿态预测
    :return:
    """
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 进行人脸检测
    detect_result2 = seetaFace.Detect(simage)
    print(detect_result2)
    face_num = detect_result2.size
    # 进行方向检测
    if face_num >= 1:
        face1 = detect_result2.data[0].pos
        points5 = seetaFace.mark5(simage, face1)  # 5特征点检测
        pose_level = seetaFace.PoseEvaluate(simage, face1, points5)
        print(pose_level)
        crop_face = seetaFace.CropFace(simage, points5)
        cv2.imwrite('./images/test.jpg', crop_face)

    return "detect_false"

def rec_test(image, feature1):
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 进行人脸检测
    detect_result2 = seetaFace.Detect(simage)
    print(detect_result2)
    face_num = detect_result2.size
    # 如果检测到一张人脸
    if face_num == 1:
        face2 = detect_result2.data[0].pos
        points = seetaFace.mark5(simage, face2)
        feature = seetaFace.Extract(simage, points)
        similar1 = seetaFace.CalculateSimilarity(feature, feature1)
        print(similar1)

def sim(image):
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 进行人脸检测
    detect_result2 = seetaFace.Detect(simage)
    print(detect_result2)
    face_num = detect_result2.size
    # 如果检测到一张人脸
    if face_num == 1:
        face2 = detect_result2.data[0].pos
        points = seetaFace.mark5(simage, face2)
        feature = seetaFace.Extract(simage, points)
        return feature


image_test = cv2.imread('./images/me.jpg')
image_test1 = Image.open('./images/me的副本.jpg')
image_test1 = sim(image_test1)
rec_test(image_test, image_test1)


def crop_extract(image):
    """
    裁剪并获取特征值
    :param img_url:
    :return:
    """
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 进行人脸检测
    detect_result2 = seetaFace.Detect(simage)
    print(detect_result2)
    face_num = detect_result2.size
    # 人脸截取
    face1 = detect_result2.data[0].pos
    points5 = seetaFace.mark5(simage, face1)  # 5特征点检测
    pose_level = seetaFace.PoseEvaluate(simage, face1, points5)
    print(pose_level)

    # 如果检测到一张人脸
    if face_num == 1:
        face2 = detect_result2.data[0].pos
        points = seetaFace.mark5(simage, face2)
        feature = seetaFace.Extract(simage, points)
        return feature
    else:
        return 'face_false'


def full_aspect_face_detect(upload_img):
    """
    全向人脸审核
    :param upload_img:前端上传图片
    :return:
    """
    first_result = pose_predict(upload_img)
    if first_result == "ok":
        return "detect_ok", upload_img

    elif first_result == "detect_false":
        revolve_time = range(1, 4)
        state = ""
        for i in revolve_time:
            print('旋转次数', i)
            sec_image = np.rot90(upload_img, i)
            # rotation angle in degree
            # sec_image = ndimage.rotate(upload_img, 90*i)
            sec_image = sec_image.astype(np.uint8)
            second_result = pose_predict(sec_image)

            # 转换回opencv图像
            if second_result == "ok":
                print(second_result)
                cv2.imwrite('./images/test2.jpg', sec_image)
                return "detect_ok", sec_image
            else:
                cv2.imwrite('./images/test000.jpg', sec_image)
                state = "unfinished"

        if state != "" and state == "unfinished":
            return "detect_false", None


