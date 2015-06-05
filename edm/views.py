from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from ipware.ip import get_ip

import time
import hashlib
import requests
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


def get_token(request, user_id):
    settings_EDM = {
        'API_KEY': 'API_ZENHEADS',
        'MAGIC_WORD': '9ce8a3919da5ffe41cc9219a1ce47242',
    }

    api_key = settings_EDM['API_KEY']
    magic = settings_EDM['MAGIC_WORD']
    ip = get_ip(request)
    # ip = '80.99.236.194'        # on local network get your ip
    timestamp = str(int(time.time()))

    m = hashlib.md5()
    to_hash = api_key + ip + timestamp + magic
    m.update(to_hash)

    data = {
        'id': api_key,
        'uid': user_id,
        'ip': ip,
        'ts': timestamp,
        'hash': m.hexdigest()
    }

    response = requests.post(url='http://api.edmdesigner.com/api/token',
                             data=data)
    # assert http 200
    return response.text


@api_view(['POST'])
def token(request):
    user_id = request.DATA['userId']
    edm_token = get_token(user_id)
    return Response(data=edm_token, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def edm_designer(request):
    context = {'edm_user': 'templater'}
    return render(request, 'edm/edm_designer.html', context)


@api_view(['POST'])
def generate(request, project_id):
    user = 'templater'
    edm_token = json.loads(get_token(request, user))['token']

    url = 'http://api.edmdesigner.com/json/project/generate/' + project_id
    params = {
        'user': user,
        'token': edm_token
    }
    try:
        response = requests.get(url=url,
                                params=params)
    except Exception as e:
        response = {'text': 'error'}
    return Response(data=response.text, status=status.HTTP_200_OK)