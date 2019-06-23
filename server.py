#!/usr/bin/env python

from aiohttp import web 
import aiohttp_jinja2
import jinja2
from cryptography import fernet
import os,base64
from aiohttp_session import setup, get_session, session_middleware,new_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_jinja2 import render_template

import argparse

cmdparser =  argparse.ArgumentParser()
cmdparser.add_argument('--node',help="link other node")
args = cmdparser.parse_args()

_storage = dict()   
_storage['node'] = []
PROJECT_ROOT = os.path.abspath('./')
# print(PROJECT_ROOT)   
@web.middleware
async def auth(request,handler):
    # print('auth middleware')
    # return web.HTTPNotFound(body="auth failed")
    response = await handler(request)
    # print(response)
    return response

# @aiohttp_jinja2.template('index.html')
async def Hello(request):
    # print('hello')
    session = await new_session(request)
    session['user'] = 'user session data'
    # print(session['user'])
    # return web.HTTPNotFound(body="404 NOT FOUND")
    name = request.match_info.get('name')
    print(request.cookies)
    # return web.Response(text='Hello {}'.format(name))
    context = {'title':'sunqi'}
    resp = render_template('index.html',request,context)
    resp.set_cookie('_L_G','FFFFFF')
    return resp

async def pro(request):
    session = await get_session(request)
    # print(session['user'])
    try:
        user = session['user']
    except KeyError:
        r = web.Response(text='pro not login')
        r.set_cookie('_gid','33223')
        return r
    else:
        r = web.Response(text='pro {}'.format(user))
        r.set_cookie('_uid','00000000')
        return r

#broadcast node info
# def broadcast():
#     for node in _storage.node:
        

# receive node
async def Version(request):
    # peername = request.transport.get_extra_info('peername')
    # if peername is not None:
    #     host, port = peername
    #     print(peername)
    try:
        assert request.header['content-type'] == 'application/json'
    except:
        return web.Response(text="invalid content type")
    print(request.content)
    data = await request.content.read()
    # print(str(request.content.read()))
    # print(dat
    return web.Response(text="version")
    # try:
    #     assert request.content != None 
    # finally:
    #     return web.Response(text='v1.0.0')

app = web.Application(middlewares=[auth])
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(str('./templates')))
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))
app.router.add_static('/static/',
                          path='./static',
                          name='static')
app.add_routes([web.get('/hello',Hello)])
app.add_routes([web.get('/pro',pro)])
app.add_routes([web.post('/ver',Version)])
web.run_app(app)


























