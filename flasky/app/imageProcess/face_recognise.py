# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 16:13:20 2018
总结该网络的输入为47x55，每次batch_size为256,16个为一组。有训练，验证，测试集
模型的超参数为学习率，AdamOptimizer方式，batch_size,激活函数，最后一层为softmax层进行分类训练时用。评价向量相似度
@author: shen1994
最终结论，人脸对齐与裁剪会很大影响人脸识别结果，特别是对于侧脸，如果不进行完美的对齐，则无法识别，
关键是如何进行正脸对齐呢，也无法解决。人脸对齐的问题已解决。侧脸完全不行。必须漏出整个脸，尤其是下巴，要不然人脸检测
不出来。计算20张图像也是1秒钟，50张也一样
关于准确率从500帧的视频中，帧率为25,时长20s，1080P，间隔取出50张图片，测得有三张没有识别出来，其他均识别出来。

"""

import tensorflow as tf
import numpy as np
from .image_vector import load_pair_vector
import time


def cosine(a, b): 
    
    t = np.float(np.dot(a.T, b))
    k = np.linalg.norm(a) * np.linalg.norm(b)
    cos = t / k
    return 1-cos


def run(threshold):
    # get last model,include meta ,data,index. model variables
    ckpt = tf.train.latest_checkpoint('model')
    saver = tf.train.import_meta_graph(ckpt + '.meta')
    
    with tf.Session() as sess:
        time_begin = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print("time_begin:%s" % time_begin)
        sess.run(tf.global_variables_initializer())
        # from meta restore variables ckpt
        saver.restore(sess, ckpt)
        x = tf.get_default_graph().get_tensor_by_name("input/x:0")
        vector = tf.get_default_graph().get_tensor_by_name("DeepID/Relu:0")
        # load test data and real data
        test_x_1, number_1 = load_pair_vector("PKL/jin_4.pkl")
        real_x_1, number_2 = load_pair_vector("PKL/origin.pkl")
        # face predict vector
        pre_vector_test = sess.run(vector, {x: test_x_1})
        pre_vector_real = sess.run(vector, {x: real_x_1})
        # get face.
        result = []
        for test in pre_vector_test:
            for index, real in enumerate(pre_vector_real):
                if cosine(test, real) < threshold:
                    result.append(index)
                    break
        result_new = set(result)
        # according face_path and username return face_name
        return result_new



