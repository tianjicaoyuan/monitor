from flask import render_template, request, jsonify
from . import main

# return 404 or 500 error


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Internal server error'})
        return response
    return render_template('500.html'), 500
