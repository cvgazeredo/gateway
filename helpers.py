from flask import request
import requests
import jwt
from typing import Dict

from jwt import DecodeError

AUTHENTICATION_SERVICE_URL = "http://127.0.0.1:8000"


def get_user_id():
    try:
        token = request.headers.get('Authorization').replace('Bearer ', '')
        decoded_token: Dict = jwt.decode(jwt=token, algorithms=['HS256'], options={"verify_signature": False})
        user_id = decoded_token.get('user_id')

        return user_id

    except BaseException:
        return ""


def authenticate():
    user_id = get_user_id()
    auth_req = f"{AUTHENTICATION_SERVICE_URL}/users/{user_id}"
    auth_header = {"Authorization": request.headers.get('Authorization')}
    auth_response = requests.get(url=auth_req, headers=auth_header)

    return auth_response
