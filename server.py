#! python3

import socket
import urllib.parse


class Request(object):
    """
    定义一个 class Request
    用来保存请求的数据
    """
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
    
    def form(self):
        # 解决 windows中文版 编码问题
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            key, value = arg.split('=')
            f[key] = value
        return f


class Message(object):
    def __init__(self):
        self.author = ''
        self.passage = ''
    
    def __repr__(self):
        return '{}: {}'.format(self.author, self.passage)


message_list = []
request = Request()


def log(*args, **kwargs):
    """
    用 log 代替 print
    """
    print('log', *args, **kwargs)


def template(filename):
    pass


def route_index():
    """
    PATH  '/'
    """
    header = 'HTTP/1.X 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello Gua!</h1><img src="dodge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    """
    PATH  '/doge.gif'
    """
    with open('doge.gif', 'r') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_message():
    """
    PATH  '/messages'
    留言板页面
    """
    log('本次请求的 method 是', request.method)
    if request.method == 'POST':
        msg = Message()
        form = request.form()
        log('Post', form)
        msg.author = form.get('Author', '')
        msg.passage = form.get('Passage', '')
        # 应该在这里保存 message_list
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    # 渲染一个模板
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{message}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    pass


def parsed_path(path):
    query = {}
    if path.find('?') == -1:
        return path, query
    else:
        path, query_lined = path.split('?', 1)
        queries = query.split('&')
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
    log('path and query', path,query)
    
    responses = {
        '/': route_index,
        '/messages': route_message,
        '/doge.gif': route_image,
    }
    response = responses.get(path, error)
    return response()


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
                # 把 body 放入 request 中
                request.body = req.split('\r\n\r\n', 1)[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容（页面）
                response = resoponse_for_path(path)
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
