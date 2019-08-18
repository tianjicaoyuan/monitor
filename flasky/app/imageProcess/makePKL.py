# -*- coding: utf-8 -*-
"""
从上传的视频中读取图片并进行人脸检测，人脸对齐，人脸裁剪，转化为PKL文件
open()函数有相对路径和绝对路径之分
"""
import pickle
import numpy as np
from PIL import Image
import cv2 as cv
import os
import time
import dlib


def crop_from_image(src_file, des_file, crop_size):
    # 将图片裁剪成特定大小,320x320原文件大小，起点32x32,终点32x8:32x9,最后resize为55x47。图片裁剪对结果影响很大。
    # 人脸并没有对齐
    img = Image.open(src_file, "r")
    img_width, img_height = img.size
    start_point_x = int(img_width / 10)
    start_point_y = int(img_height / 10)
    x_move = int(img_width /10) * 8
    y_move = start_point_y + int(img_height / 10)*8
    box = (start_point_x, start_point_y, x_move, y_move)
    img_crop = img.crop(box)
    img_resize_crop = img_crop.resize(crop_size)
    img_resize_crop.save(des_file)


def folder_for_crop(db_folder, result_folder, crop_size):
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    # 目标文件夹不存在，则新建在image下
    # 每个vedio文件夹下存储着图像文件，对图像文件进行裁剪
    # src为原图像，des为裁剪后的图像，最后结果就是生成两个文件夹
    # origin为原始数据集，result为裁剪后的数据集。
    number = 0
    for img_file in os.listdir(db_folder):
        number += 1
        src_img_path = db_folder + os.sep + img_file
        des_img_path = result_folder + os.sep + img_file
        crop_from_image(src_img_path, des_img_path, crop_size)


def vector_counter(image_folder):
    # 记录cvs文件的行数，如果是size的整数，则返回size。如果不是，使其成为size的整数。
    count = 0
    for image in os.listdir(image_folder):
        count = count+1
    return count


# 将图片以可读形式，读取数据。
def image_to_vector(image_path):
    with Image.open(image_path, "r") as image:
        array_image = np.array(image, dtype="float32")
        return array_image


# 将视频中人脸图转化为pkl序列化，不带标签
def image_pkl_2(image_folder, pkl_path):
    # 计算人脸图的个数,20张图像序列化1秒钟，50张也是一秒钟
    time_begin = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    vector_number = vector_counter(image_folder)
    # 人脸图总向量
    pkl_file = open(pkl_path, "wb")
    pickle.dump((vector_number, 1, 1), pkl_file, pickle.HIGHEST_PROTOCOL)
    for image_path in os.listdir(image_folder):
        x_1 = []
        src_path = image_folder + os.sep + image_path
        x_1.append(image_to_vector(src_path))
        pickle.dump(np.asarray(x_1, dtype="float32"), pkl_file, pickle.HIGHEST_PROTOCOL)
    pkl_file.close()
    time_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("time_begin:%s" % time_begin)
    print("time_end:%s" % time_end)


def get_faces(image_folder, face_folder):
    # 导入人脸检测模型，如何准确检测出人脸，并框出来，并进行对齐很重要。人脸是否检测到与原图像大小有关。
    # 640x480大小的图片可检测到17张人脸，从50张中。人脸检测的算法并不理想。所花时间为6s。
    # 如果不是整个人脸出现，则完全检测不出来，缺了一点都不行，垃圾人脸检测算法。
    # 运用cnn模型的人脸检测算法比原来的检测算法好多了，除了用手挡住嘴巴检测不出来后，侧脸并且对齐效果也很强，就是用CPU计算耗费时间长
    # 50张图片用时23分钟。需要开启GPU加速，进行处理，这样才不会慢。检测+识别640X480像素的视频流一秒钟大约十几帧。
    if not os.path.exists(face_folder):
        os.mkdir(face_folder)
    time_begin = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # detector = dlib.get_frontal_face_detector()
    detector = dlib.cnn_face_detection_model_v1('harr/mmod_human_face_detector.dat')
    # 导入检测人脸特征点的模型
    sp = dlib.shape_predictor('harr/shape_predictor_68_face_landmarks.dat')
    # 读入图片
    for image_path in os.listdir(image_folder):
        print(image_path)
        src_path = image_folder + os.sep + image_path
        des_path= face_folder + os.sep + image_path
        bgr_img = cv.imread(src_path)
        if bgr_img is None:
            print("Sorry, we could not load '{}' as an image")
            exit()
    # opencv的颜色空间是BGR，需要转为RGB才能用在dlib中
        else:
            rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
            # 检测图片中的人脸
            dets = detector(rgb_img, 1)
            # 识别人脸特征点，并保存下来
            faces = dlib.full_object_detections()
            for det in dets:
                faces.append(sp(rgb_img, det.rect))
            if faces:
                # 人脸对齐
                images = dlib.get_face_chips(rgb_img, faces, size=320)
                for image in images:
                    cv_rgb_image = np.array(image).astype(np.uint8)
                    # 先转换为numpy数组
                    cv_bgr_image = cv.cvtColor(cv_rgb_image, cv.COLOR_RGB2BGR)
                    # opencv下颜色空间为bgr，所以从rgb转换为bgr
                    cv.imwrite(des_path, cv_bgr_image)
            else:
                print("miss %s" % (image_path) )
    time_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print("time_begin:%s" % time_begin)
    print("time_end:%s" % time_end)


def get_images(video_path, image_folder):
    # 从视频中提取每一张人脸图片保存在图片文件夹中。读取图片50张所花时间5秒，读取100张10s。
    # 必须争取在20s内处理该视频。读取并裁剪为640x480
    if not os.path.exists(image_folder):
        os.mkdir(image_folder)
    camera = cv.VideoCapture(video_path)
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    times = 0
    count = 0
    while True:
        times += 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times % 10 == 0:
            count += 1
            x, y = image.shape[0:2]
            crop_image=cv.resize(image, (640, 480), interpolation=cv.INTER_LINEAR)
            cv.imwrite(image_folder + os.sep+str(count) + '.jpg', crop_image)
            print(image_folder + os.sep+str(times) + '.jpg')
    print('图片提取结束')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    camera.release()


def video_to_pkl(video_path):
    get_images(video_path, 'src_image')
    get_faces('src_image', 'face_image')
    folder_for_crop('face_image', 'cut_image', (47, 55))
    image_pkl_2('cut_image', 'PKL/jin_4.pkl')
    # read pkl vector to image show
    # pkl_file = open('image/test_vector_dataset.pkl', "rb")
    # big_number, size, v_number = pickle.load(pkl_file)
    # print(big_number,size,v_number)
    # real_x_1=pickle.load(pkl_file)
    # pkl_file.close()
    # pylab.imshow(np.asarray(real_x_1[1], dtype="int32"))
    # pylab.gray()
    # pylab.show()
