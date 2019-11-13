#coding=utf-8
from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify

def error_response(status_code, msg=None):
    payload = {"error": HTTP_STATUS_CODES.get(status_code, 'Unknow error')}
    if msg:
        payload['message'] = msg
    response = jsonify(payload)
    response.status_code = status_code
    return response
