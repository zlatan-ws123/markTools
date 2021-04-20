import cv2
import os
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
import sys
import csv
from pathlib import Path

def cv2Img(path, index, size):
    vedioPath = path
    cap = cv2.VideoCapture(vedioPath)
    length = size
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(1, index)
    ret, frame = cap.read()
    cap.release()
    if type(frame)==type(None):
        return False, False
    cropIndex = max(frame.shape[0], frame.shape[1])/length
    if frame.shape[0] >= frame.shape[1]:
        newFrame = cv2.resize(frame, (int(frame.shape[1]/cropIndex), length))
    else:
        newFrame = cv2.resize(frame, (length, int(frame.shape[0]/cropIndex)))
    shrink = cv2.cvtColor(newFrame, cv2.COLOR_BGR2RGB)
    '''
    # opencv转换成qt格式这里暂时用不到
    qtImg = QImage(shrink.data,  # 数据源
        shrink.shape[1],  # 宽度
        shrink.shape[0],  # 高度
        shrink.shape[1] * 3,  # 行字节数
        QImage.Format_RGB888)
    '''
    return shrink, frame_count

def saveFrame(data, fileName):
    try:
        newData = list(map(int, data))
        # strData = str(newData).replace("[", "").replace(" ", "").replace("]", "")
        newFileName = fileName.split(".", 1)[0] + ".csv"
        if Path(newFileName).exists():
            return False
        with open(newFileName, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(newData)
            return True
    except:
        return False

if __name__=="__main__":
    # path = r"/home/oem/Desktop/test5-jack-2021-04-13/videos/扭体croppedDLC_mobnet_100_test5Apr13shuffle1_750000_labeled.mp4"
    # qtImg = cv2Qpix(path)
    pass