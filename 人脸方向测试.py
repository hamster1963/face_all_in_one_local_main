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





def pose_predict(image):
    """
    人脸姿态预测
    :return:
    """
    simage = get_seetaImageData_by_numpy(image)  # 原图转SeetaImageData
    # 进行人脸检测
    detect_result2 = seetaFace.Detect(simage)
    print(detect_result2)

pose_predict('./images/4.jpg')