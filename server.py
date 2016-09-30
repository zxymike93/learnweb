#! python3
# coding: utf-8

import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict as route_dict_main
from routes_weibo import route_dict as route_dict_weibo
from routes_todo import route_dict as route_dict_todo
from routes_api_todo import route_dict as route_dict_api_todo


class Request(object):
    """
    定义一个 class Request
    用来保存请求的数据
    对于 Cookies 需要额外的处理
    所以添加 headers 和 cookies
    """
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_headers(self, header):
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 调用 add_cookies 要在循环外面
        # 否则 'Cookie' 会被覆盖
        self.add_cookies()

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        cks = cookies.split('; ')
        # log('all cookies', cks)
        for ck in cks:
            if '=' in ck:
                k, v = ck.split('=')
                self.cookies[k] = v

    def form(self):
        # 解决 windows中文版 编码问题
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            key, value = arg.split('=')
            f[key] = value
        return f


request = Request()


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    query = {}
    if path.find('?') == -1:
        return path, query
    else:
        path, query_lined = path.split('?', 1)
        queries = query_lined.split('&')
        for i in queries:
            key, value = i.split('=')
            query[key] = value
        return path, query


def response_for_path(path):
    """
    根据 path 调用响应的处理函数
    没有处理的 path 会返回 404
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    # log('path and query', path, query)
    
    responses = {
        '/static': route_static,
    }
    responses.update(route_dict_main)
    responses.update(route_dict_weibo)
    responses.update(route_dict_todo)
    responses.update(route_dict_api_todo)
    response = responses.get(path, error)
    return response(request)


def run(host='', port=3000):
    """
    运行程序（即 启动服务器）
    """
    # 初始化 socket 的套路，先记住
    # 使用 with 可以保证程序终端的时候正确关闭 socket 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            # 监听/接收/读取 请求数据，编码成字符串
            s.listen(3)
            # accept() 接收来自 client 的连接
            # 用 Request类 储存
            connection, address = s.accept()
            req = connection.recv(1024)
            req = req.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, req))
            # try..except.. 排除会引起异常的请求
            try:
                # chrome 会发空请求导致 split 得到空 list
                # 用 try 放置程序崩溃
                path = req.split()[1]
                # 设置 request 的 method
                request.method = req.split()[0]
                # 把 headers 第一行的请求行去掉之后再传入 add_headers
                request.add_headers(req.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
                # 把 body 放入 request 中
                request.body = req.split('\r\n\r\n', 1)[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容（页面）
                response = response_for_path(path)
                # Send response to Client
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            # 处理完请求，关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
