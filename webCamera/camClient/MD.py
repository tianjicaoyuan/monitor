# -*- coding:utf-8 -*-
import logging
import time, random
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
import requests
import datetime as dt
import io
from PIL import Image
import sqlite3

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')


class ViBe:
    __defaultNbSamples = 20
    # 每个像素点的样本个数
    __defaultReqMatches = 2
    # min指数判断是否为背景点的最小匹配个数
    __defaultRadius = 20
    # 判断是否匹配的像素半径
    __defaultSubsamplingFactor = 16
    # 子采样率
    __BG = 0
    # 背景像素
    __FG = 255
    # 前景像素
    __c_xoff = [-1, 0, 1, -1, 1, -1, 0, 1, 0]
    # 像素点的8领域
    __c_yoff = [-1, 0, 1, -1, 1, -1, 0, 1, 0]

    __samples = []
    # 背景模型中每个像素点的样本集
    __Height = 0
    # 图像高度
    __Width = 0
    # 图像宽度

    def __init__(self, grayFrame):
        '''''
        Constructor
        '''
        self.__Height = grayFrame.shape[0]
        self.__Width = grayFrame.shape[1]

        for i in range(self.__defaultNbSamples + 1):
            self.__samples.insert(i, np.zeros((grayFrame.shape[0], grayFrame.shape[1]), dtype=grayFrame.dtype))

        self.__init_params(grayFrame)

    def __init_params(self, grayFrame):

        rand = 0
        r = 0
        c = 0
        # 构建第一帧图像作为背景模型，通过对每一个像素点的8领域的随机选择作为每一个像素点的样本集
        for y in range(self.__Height):
            for x in range(self.__Width):
                for k in range(self.__defaultNbSamples):

                    rand = random.randint(0, 8)
                    r = y + self.__c_yoff[rand]
                    if r < 0:
                        r = 0
                    if r >= self.__Height:
                        r = self.__Height - 1
                    c = x + self.__c_xoff[rand]
                    if c < 0:
                        c = 0
                    if c >= self.__Width:
                        c = self.__Width - 1

                    self.__samples[k][y, x] = grayFrame[r, c]
            self.__samples[self.__defaultNbSamples][y, x] = 0


    def update(self, grayFrame):
        # 前景
        foreground = np.zeros((self.__Height, self.__Width), dtype=np.uint8)
        counts =0
        # 针对当前帧的每一个像素进行处理
        for y in range(self.__Height):
            for x in range(self.__Width):
                count = 0
                index = 0
                dist = 0.0
                # 记录像素点与背景模型中对应像素点的样本点匹配个数
                while (count < self.__defaultReqMatches) and (index < self.__defaultNbSamples):
                    dist = float(grayFrame[y, x]) - float(self.__samples[index][y, x])
                    if dist < 0: dist = -dist
                    if dist < self.__defaultRadius: count = count + 1
                    index = index + 1
                # 判断为背景点
                if count >= self.__defaultReqMatches:
                    # 将样本集中第20个样本点的值取为0
                    self.__samples[self.__defaultNbSamples][y, x] = 0
                    # 将该点取为背景点
                    foreground[y, x] = self.__BG
                    # 从0-16中随机选择一个数
                    rand = random.randint(0, self.__defaultSubsamplingFactor)
                    if rand == 0:
                        # 从样本集中随机选择一个点的指进行更新为该当前帧像素值
                        rand = random.randint(0, self.__defaultNbSamples)
                        self.__samples[rand][y, x] = grayFrame[y, x]
                    rand = random.randint(0, self.__defaultSubsamplingFactor)
                    if rand == 0:
                        # 将该点领域的一个点的样本集中的一点取为当前像素点的值
                        rand = random.randint(0, 8)
                        yN = y + self.__c_yoff[rand]
                        if yN < 0: yN = 0
                        if yN >= self.__Height: yN = self.__Height - 1
                        rand = random.randint(0, 8)
                        xN = x + self.__c_xoff[rand]
                        if xN < 0: xN = 0
                        if xN >= self.__Width: xN = self.__Width - 1
                        rand = random.randint(0, self.__defaultNbSamples)
                        self.__samples[rand][yN, xN] = grayFrame[y, x]
                else:
                    # 为非背景点，将其取为前景
                    foreground[y, x] = self.__FG
                    counts = counts+1
                    # 将当前像素的样本集的第20个点的值加1
                    self.__samples[self.__defaultNbSamples][y, x] += 1
                    # 若该店值大于50，
                    if self.__samples[self.__defaultNbSamples][y, x] > 50:
                        rand = random.randint(0, self.__defaultNbSamples)
                        if rand == 0:
                            # 随机选一个样本点值取为当前点的值
                            rand = random.randint(0, self.__defaultNbSamples)
                            self.__samples[rand][y, x] = grayFrame[y, x]
        return counts, foreground

def record_video():
	with PiCamera() as camera:
		camera.resolution=(1920,1080)
		camera.hflip=True
		camera.vflip=True
		camera.framerate=25
		camera.annotate_background=camera.Color('black')
		camera.annotate_text=dt.now().strftime('%Y-%m-%d %H:%M:%S')
		camera.start_preview()
		time.sleep(3)
		camera.start_recording('jin.h264')
		camera.wait_recording(17)
		camera.stop_recording()
		camera.stop_preview()
		fp = open('/home/pi/Documents/camWebServer/jin.h264','rb')
		files = {'video': fp}
		time=dt.now().strftime('%Y-%m-%d %H:%M:%S')
		videoPath = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
		cameraName='1-'
		video_info={'cameraName':cameraName, 'time':time, 'videoPath':videoPath}
		r = requests.post("http://172.20.10.11:5000/upload", data=video_info, files=files)
		fp.close()
		os.remove('/home/pi/Documents/camWebServer/jin.h264')
	
def moveDe():
	with PiCamera() as camera:
		camera.resolution = (640,480)
		camera.framerate = 25
		camera.hflip =True
		camera.vflip = True
		time.sleep(2)
		count=1
		for frame in camera.capture_continuous('jin.jpg', format='jpeg',use_video_port=True):
			if count == 1:
				im=Image.open(frame).convert("L")
				x, y = im.size
				imResize = im.resize((int(x / 4), int(y / 4)))
				gray=np.array(imResize)
				print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
				vibe =ViBe(gray)
				print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
				# need 12 seconds,modelUpgrade need 1s
				count = count+1
			else:
				count = count + 1
				print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
				im=Image.open(frame).convert("L")
				x, y = im.size
				imResize = im.resize((int(x / 4), int(y / 4)))
				gray=np.array(imResize)
				sum = int(y/2)*int(x/2)
				counts, foreground =vibe.update(gray)
				print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
				percent = str(counts/sum)[:4]
				if((counts/sum)<0.01):
					logging.info(percent + '  Normal')
				else:
					logging.info(percent + '  MotionException')
					break
		camera.resolution=(1920,1080)
		camera.annotate_background=camera.Color('black')
		camera.annotate_text=dt.now().strftime('%Y-%m-%d %H:%M:%S')
		camera.start_preview()
		camera.start_recording('jin.h264')
		camera.wait_recording(17)
		camera.stop_recording()
		camera.stop_preview()
		fp = open('/home/pi/Documents/camWebServer/jin.h264','rb')
		files = {'video': fp}
		time=dt.now().strftime('%Y-%m-%d %H:%M:%S')
		videoPath = dt.now().strftime('%Y-%m-%d-%H-%M-%S')
		cameraName='1-'
		video_info={'cameraName':cameraName, 'time':time, 'videoPath':videoPath}
		r = requests.post("http://172.20.10.11:5000/upload", data=video_info, files=files)
		fp.close()
		os.remove('/home/pi/Documents/camWebServer/jin.h264')
		return True

		
def create_db():
	db = sqlite3.connect('jin.db')
	c = db.cursor()
	c.execute('''CREATE TABLE CAMERA
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           CHAR(10)    NOT NULL,
       MOVE            INT     NOT NULL,
       ADDCAMERA       INT,    NOT NULL
       INFO        CHAR(50));''')
	c.execute("INSERT INTO CAMERA (ID,NAME,MOVE,ADDCAMERA,INFO) VALUES (1, '1', 1, 0, 'NO' )")
	db.commit()
	db.close()
	
def testCameraIsOnLine(ipaddress):
    try:
        html = requests.get(ipaddress, timeout=2)
    except:
        return False
    return True

	
if __name__ == '__main__':
	while True:
		if testCameraIsOnLine(ipaddress):
			moveDe()
		else:
			time.sleep(60)