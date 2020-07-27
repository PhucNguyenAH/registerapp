from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl

import snowboydecoder
import sys
import cv2
import os
import json
import numpy as np
import requests
import pyaudio
from queue import Queue
from io import BytesIO
import time
import struct
import wave
import pickle
import tkinter as tk
sensitivity = 0.7
model_file = './computer.umdl'
detection = snowboydecoder.HotwordDetector(model_file, sensitivity=sensitivity)


# GUI of register app
from ui_jetsonWindow import *

queue = Queue()
def callback(in_data, frame_count, time_info, status):
    queue.put(in_data)
    return (in_data, pyaudio.paContinue)
  
# First window for filling ID
class JetsonWindow(QMainWindow):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_JetsonWindow()
        self.ui.setupUi(self)
    
        self.root = tk.Tk()
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        self.hotword = 0
        self.faceres = []
        self.voiceframes = []
        self.record = 0
        
        self.server_url = 'http://172.20.10.3:5001/'
        self.p = None
        self.p1 = None
        self.stream = None
        self.stream1 = None
        self.list = ['1752015', '1752259', '1752041', 'NOT INDENTIFIED']
        self.image = None
        self.req=1
        self.rep=0
        self.encapsulate_face = None

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function that check temporary ID
        self.timer.timeout.connect(self.Attendance)
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)
        # self.cap.set(3, self.h)
        # self.cap.set(4, self.w)
        self.timer.start(20)
    
    def gstreamer_pipeline(self,
        capture_width=1280,
        capture_height=720,
        display_width=1280,
        display_height=720,
        framerate=90,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

    def Attendance(self):
        if self.record ==0:
            # self.detection = snowboydecoder.HotwordDetector(self.model_file, sensitivity=self.sensitivity)
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(
                            rate=16000,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=512,
                            input_device_index=11,
                            stream_callback = callback
            )
            self.stream.start_stream()
            self.record =1

        # Begin taking photo            
        # read image in BGR format
        ret, self.image = self.cap.read()
        # cv2.imshow('frame', image)
        left=0
        right=0
        top=0
        bottom=0
        encapsulate_face = pickle.dumps(self.image, protocol=pickle.HIGHEST_PROTOCOL)
        
        # if face_response['data']:
        #     self.faceres = face_response
        
        # if self.faceres['box']:
        #     left, right, top, bottom = tuple(self.faceres['box'])
        #     cv2.rectangle(image, (left, top), (right, bottom), (250, 0, 0),2)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = self.image.shape
        step = channel * width
                    
        # create QImage from image
        qImg = QImage(self.image.data, width, height, step, QImage.Format_RGB888)

        # show image in img_label
        wi = self.ui.image_label.width()
        he = self.ui.image_label.height()
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg).scaled(wi, he, QtCore.Qt.KeepAspectRatio))
        if queue.qsize() > 0:
            while queue.qsize() > 32:
                queue.get()
            buff = []
            if queue.qsize() >= 32:
                while queue.qsize() > 0:
                    buff.append(queue.get())
            ans = detection.detector.RunDetection(b''.join(buff))
            print(f'ans {ans}')
            print(f'hotword {self.hotword}')
            if ans==1:
                self.hotword = 1
                self.p.terminate()
                self.stream.close()
                self.p1 = pyaudio.PyAudio()
                self.stream1 = self.p1.open(
                        rate=16000,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=512,
                        input_device_index=11,
                )
                self.stream1.start_stream()
                ans=0
                name = "Device 1 \n Recording"
                self.ui.infor_label.setText(name)
                print(f'ans {ans}')
                print(f'hotword {self.hotword}')
            elif self.hotword==1:
                print("Recording")
                # self.p1 = pyaudio.PyAudio()
                # self.stream1 = self.p1.open(
                #         rate=16000,
                #         channels=1,
                #         format=pyaudio.paInt16,
                #         input=True,
                #         frames_per_buffer=512,
                #         input_device_index=11,
                # )
                # self.stream1.start_stream()
                self.record = self.record + 1
                print(self.record)
                
                
                for i in range(0, int(16000/512*3)):
                    self.voiceframes.append(self.stream1.read(512))
                # if self.record == 4:
                print("Done record")
                name = "Device 1 \n Done record"
                self.ui.infor_label.setText(name)
                self.faceres = []
                self.hotword = 0
                self.record = 0
                self.p1.terminate()
                self.stream1.close()
                face_response = requests.post(self.server_url+'face', data=encapsulate_face).json()
                if face_response['data']:
                    face_result = np.array(face_response['data'])
                encapsulate_voice = pickle.dumps(self.voiceframes, protocol=pickle.HIGHEST_PROTOCOL)
                voice_response = requests.post(self.server_url+'voice', data=encapsulate_voice).json()['data']
                voice_result = np.array(voice_response)
                # result =  np.add(face_result*0.8, voice_result*0.2)
                result = 2*face_result*voice_result/(face_result+voice_result)
                if np.any(result > 0.9):
                    name = "Device 1 \n" + self.list[result.argmax()] + f': {round(result[result.argmax()] * 100 , 1)}'
                else:
                    name = "Device 1 \n" + self.list[-1]
                self.ui.infor_label.setText(name)
                self.voiceframes = []
        return 0
        




if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = JetsonWindow()
    mainWindow.showFullScreen()
    # mainWindow.show()

    sys.exit(app.exec_())
