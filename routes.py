#!/usr/bin/env python3

from utils import log
from models import User, Message

import random

message_list = []
# session 字典里 每个随机生成的'session_id' 对应一个 'username'
session = {}


def random_str():
    """
    生成随机字符串的函数
     用来生成 session_id
    """
    seed = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    s = ''
    for i in range(7):
        random_index = random.randint(0, len(seed)-1)
        s += seed[random_index]
    return s


def template(filename, **kwargs):
    """
    读取 html 模板文件
    要转为 utf-8 编码
    原来 boby 里面的 replace 放到这里
    占位符当作参数传入
    """
    path = 'templates/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
        for k, v in kwargs.items():
            t = t.replace('{{' + k + '}}', str(v))
        return t


def redirect(location):
    headers = {
        'Content-Type': 'text/html',
    }
    headers['Location'] = location
    header = response_with_header(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, 'guest')
    return username


def route_index(request):
    """
    PATH  '/'
    """
    header = 'HTTP/1.X 200 OK\r\nContent-Type: text/html\r\n'
    username = current_user(request)
    body = template('index.html'， username=username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_header(headers, status_code=200):
    # status_code 应该有个字典，有对应的描述
    header = 'HTTP/1.x {} OK\r\n'.format(status_code)
    #  \r\n 不放在 join 前面，保证每个 header 都换行
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'user=gua; height=169',
    }
    username = current_user(request)
    if request.method == 'POST':
        # log('login, self.headers', request.headers)
        log('login, self.cookies', request.cookies)
        form = request.form()
        usr = User(form)
        if usr.validate_login():
            # session 使 cookie 不能被轻易伪造
            session_id = random_str()
            session[session_id] = usr.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = 'True'
        else:
            result = 'False'
    else:
        result = ''
    body = template('login.html', result=result, username=username)
    # Set-Cookie 是在登录成功之后发送，所以在响应前生成 header
    header = response_with_header(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.X 200 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        usr = User(form)
        if usr.validate_register():
            # log('DEBUG-form-usr', usr)
            usr.save()
            result = 'True<br/> <pre>{}</pre>'.format(User.all())
        else:
            result = 'Username and Password must longer than 3 words.'
    else:
        result = ''
    body = template('register.html', result=result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_profile(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    if username == 'guest':
        return redirect('/')
    else:
        header = response_with_header(headers)
    # 返回当前用户的实例，以便后面调用它的属性
    user = User.find_by(username=username)
    body = template('profile.html',
                     id=user.id,
                     username=user.username,
                     note=user.note)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_static(request):
    """
    PATH  '/doge.gif'
    """
    filename = request.query.get('file', '')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_message(request):
    """
    PATH  '/messages'
    留言板页面
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'user=gua; height=169',
        # 'Location': '/message',
    }
    log('本次请求的 method 是', request.method)
    username = current_user(request)
    if username == 'guest':
        # 如果用户没登录，重定向到 login 页面
        return redirect('/')
    else:
        header = response_with_header(headers)
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    #  渲染一个模板
    msgs = '<br>'.join([str(m) for m in message_list])
    body = template('html_basic.html', messages=msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/message': route_message,
    '/login': route_login,
    '/register': route_register,
    '/profile': route_profile,
}