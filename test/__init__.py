import pytest,json, logging
from flask import Flask, request

from blueprints import app
from app import cache

def call_client(request):
    client=app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token_buyer():
    token = cache.get('test-token-internal')
    if token is None:
        data={
            'nama' : 'aul',
            'password': 'abc'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-internal', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_seller():
    token = cache.get('test-token-non-internal')
    if token is None:
        data={
            'nama' : 'syamsul',
            'password': 'abc'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-non-internal', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token

def create_token_not_enough_saldo():
    token = cache.get('test-token-not-enough-saldo')
    if token is None:
        data={
            'nama' : 'tes',
            'password': 'tes'
        }

        req = call_client(request)
        res = req.post('/welcome/login',json=data)

        res_json=json.loads(res.data)

        logging.warning('RESULT :%s', res_json)

        assert res.status_code == 200

        cache.set('test-token-not_enough_saldo', res_json['token'],timeout=60)

        return res_json['token']
    else:
        return token