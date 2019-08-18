from flask import render_template, session, redirect, url_for, request, flash, Response
from . import main
from .forms import IcloudForm
from .. import db
from ..models import Uxser, Video, Camera
from flask_login import current_user, login_required
import os, requests,time,cv2
import subprocess, multiprocessing
from ..imageProcess import makePKL, face_recognise

# for a ip_address,return whether it is online


def test_camera_online(ip_address):
    try:
        html = requests.get(ip_address, timeout=2)
    except:
        return False
    return True


# main html
@main.route('/')
@login_required
def index():
    # 提取数据库中的摄像机型号，和其IP地址。作为变量传入index页面中
    camera = Camera.query.all(username=current_user.username)
    posts = camera
    cameraAddress=[]
    for post in posts:
        if test_camera_online(post.cameraIpAddress):
            cameraAddress.append(post)
    if posts is None:
        flash("please add a Camera!")
    return render_template('index.html', cameraAddress=cameraAddress)


# user html
@main.route('/user/<username>')
@login_required
def user(username):
    user = Uxser.query.filter_by(username=username).first()
    if user is None:
        return render_template('404.html')
    return render_template('user.html', user=user)


# cloud video html
@main.route('/cloud', methods=['GET', 'POST'])
@login_required
def cloud():
    form = IcloudForm()
    NewQury = Video.query.order_by(Video.dateTime.desc())
    if session.get('known'):
        NewQury = Video.query.filter(Video.dateTime.between(session['StartDate'],
        session['EndDate'])).order_by(Video.dateTime.desc())
    if form.validate_on_submit():
        result = Video.query.filter(Video.dateTime.between(form.StartDate.data,
        form.EndDate.data)).order_by(Video.dateTime.desc())
        if not result.all():
            session['known'] = False
        else:
            session['known'] = True
            session['StartDate'] = form.StartDate.data
            session['EndDate'] = form.EndDate.data
        return redirect(url_for('main.cloud'))
    page = request.args.get('page', 1, type=int)
    pagination = NewQury.paginate(page, per_page=7, error_out=False)
    posts = pagination.items
    return render_template('Cloud.html', form=form, known=session.get('known'),
                           pagination=pagination, posts=posts)


# upload video html
@main.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['video']
    cameraName = request.form['cameraName']
    Time = request.form['time']
    videoPath = request.form['videoPath']
    if upload_file:
        filename = cameraName + videoPath
        # notice picpath about absolutely path or relatively path
        picpath = os.path.join('uploads/', filename)
        fp = open('static/' + picpath + '.h264', 'wb')
        fp.write(upload_file.read())
        fp.close()
        subprocess.call("D:/soft/ffmpeg/bin/ffmpeg.exe -i %s %s" % \
                        ('static/' + picpath+'.h264', 'static/' + picpath+'.mp4'), shell=True)
        camera = Camera.query.all(cameraName=cameraName).first()
        if camera.FaceRecognition == 'true':
            # 将人脸识别的结果转化为字符串，并存入video的数据库中
            makePKL.video_to_pkl('static/' + picpath+'.mp4')
            face_result = face_recognise.run(0.43)
            video = Video(cameraName=cameraName, dateTime=Time,
                          VideoPath=picpath + '.mp4', username=current_user.username, video_info=' '.join(face_result))
            db.session.add(video)
        return "success"
    else:
        return "false"


# get camera_address to see video from camera
@main.route('/video_view/<cameraName>', methods=['GET', 'POST'])
@login_required
def video_view(cameraName):
    camera = Camera.query.filter_by(username=current_user.username, cameraName=cameraName).first()
    camera_address = camera.cameraIpAddress
    camera_video_way = camera.video_way
    if camera_video_way == "False":
        return render_template('movie.html', camera_address=camera_address)

    return render_template('movie2.html', camera_address=camera_address)

