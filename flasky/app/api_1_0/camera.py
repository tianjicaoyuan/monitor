from ..models import Camera, Video
from . import api
from ..import db

from flask import request,jsonify, make_response
import requests
# for a ipaddress,return whether it is online


def testCameraIsOnLine(ipaddress):
    try:
        html = requests.get(ipaddress, timeout=2)
    except:
        return False
    return True


def jsonToResponse(data):
    result_text = jsonify(data)
    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@api.route('/GetCamera', methods=['Get','POST'])
def camera():
    username = request.form['username']
    if Camera.query.filter_by(username=username).first() is None:
        data = {"success": "false"}
        return jsonToResponse(data)
    cameraAddress = []
    camera = Camera.query.filter_by(username=username).all()
    for post in camera:
        if testCameraIsOnLine(post.cameraIpAddress):
            a = {"cameraName": post.cameraName, "cameraIpAddress": post.cameraIpAddress, "statue": "online"}
        else:
            a = {"cameraName": post.cameraName, "cameraIpAddress": post.cameraIpAddress, "statue": "offline"}
        cameraAddress.append(a)
    data = {"success": "true", "cameraAddress": cameraAddress}
    return jsonToResponse(data)


@api.route('/GetCloud', methods=['Get', 'POST'])
def cloud():
    check = request.form['check']
    cameraName = request.form['cameraName']
    page = request.form['page']
    page = int(page)
    username = request.form['username']
    if check == "false":
        NewQury = Video.filter_by(username=username, cameraName=cameraName).order_by(Video.dateTime.desc())
        pagination = NewQury.paginate(page, per_page=6, error_out=False)
        page_content = pagination.items
        page_count = pagination.pages
        pageContent = []
        if page_content is None:
            data = {"success": "false", "page_count": 1, "page_content": []}
            return jsonToResponse(data)
        for post in page_content:
            a = {"cameraName": post.cameraName, "PicturePath": post.PicturePath, "dateTime": post.dateTime.strftime('%Y-%m-%d %H:%M:%S')}
            pageContent.append(a)
        data = {"success": "true", "page_count": page_count, "page_content": pageContent}
        return jsonToResponse(data)
    beginTime = request.form['beginTime']
    endTime = request.form['endTime']
    NewQury = Video.query.filter_by(username=username, cameraName=cameraName). \
        filter(Video.dateTime.between(beginTime, endTime)).order_by(Video.dateTime.desc())
    pagination = NewQury.paginate(page, per_page=6, error_out=False)
    page_content = pagination.items
    page_count = pagination.pages
    if page_content is None:
        data = {"success": "false",  "page_count": 1, "page_content": []}
        return jsonToResponse(data)
    pageContent = []
    for post in page_content:
        a = {"cameraName": post.cameraName, "PicturePath": post.PicturePath, "dateTime": post.dateTime.strftime('%Y-%m-%d %H:%M:%S')}
        pageContent.append(a)
    data = {"success": "true", "page_count": page_count, "page_content": pageContent}
    return jsonToResponse(data)
