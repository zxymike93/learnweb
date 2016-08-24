#!/usr/bin/env python3

from utils import log
from models import Message


message_list = []

def template(filename):
    """
    读取 html 模板文件
    要转为 utf-8 编码
    """
    path = 'templates/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    PATH  '/'
    """
    header = 'HTTP/1.X 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
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
    log('本次请求的 method 是', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    # 渲染一个模板
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
