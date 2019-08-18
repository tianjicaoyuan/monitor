#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18

from flask import Flask, render_template, Response, request, jsonify
from camera_pi import camera
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'

def jsonToResponse(data):
	# 解决浏览器跨域访问问题
	result_text = jsonify(data)
	rst = make_response(result_text)
	rst.headers['Access-Control-Allow-Origin'] = '*'
	return rst

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    rst = Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
	rst.headers['Access-Control-Allow-Origin']= '*'
	return rst
	
@app.route('/addCamera',methods=['GET','POST'])
def addCamera():
	netWorkName = request.form['netWorkName']
	password = request.form['password']
    if not all([netWorkName,password]):
        subprocess.call('chmod +x /etc/wpa_supplicant/input_network.sh',shell=True)
        p1=subprocess.Popen(['/etc/wpa_supplicant/input_network.sh',netWorkName,password])
		p1.wait()
        subprocess.call('chmod +x /etc/dhcpcd.sh',shell=True)
        p2=subprocess.Popen('/etc/dhcpcd.sh')
		p2.wait()
        subprocess.call('chmod +x /etc/network/interfaces.sh',shell=True)
        p3=subprocess.Popen('/etc/network/interfaces.sh')
		p3.wait()
		#sudo service hostapd restart
		#sudo service udhcpd start
		#sudo service networking restart
        subprocess.Popen("sudo reboot",shell=True)
		data = {'success':'true'}
        return jsonToResponse(data)
    return render_template('Camera.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True, threaded=True)
