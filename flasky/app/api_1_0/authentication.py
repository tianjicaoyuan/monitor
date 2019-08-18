from flask_httpauth import HTTPTokenAuth
from ..models import Uxser
from .errors import unauthorized
from . import api
from flask import request, jsonify, make_response
from ..import db
auth = HTTPTokenAuth()


# ajax different url visited to solve
def jsonToResponse(data):
    result_text = jsonify(data)
    rst = make_response(result_text)
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if Uxser.query.filter_by(email=email).first() is None:
        data = {'success': 'false', "message": "email is not exist"}
        return jsonToResponse(data)
    user = Uxser.query.filter_by(email=email).first()
    if user.verify_password(password):
        global current_user
        current_user = user.get_username()
        data = {'success': 'true', 'username': current_user}
        return jsonToResponse(data)
    data = {'success': 'false', "message": "password is not right"}
    return jsonToResponse(data)


@api.route('/register', methods=['POST'])
def new_user():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    if Uxser.query.filter_by(username=username).first() is not None:
        data = {'success': 'false', "message": "username is  exist"}
        return jsonToResponse(data)
    if Uxser.query.filter_by(email=email).first() is not None:
        data = {'success': 'false', "message": "email is  exist"}
        return jsonToResponse(data)

    user = Uxser(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    data = {'success': 'true'}
    return jsonToResponse(data)

