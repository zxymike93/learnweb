#! python3

import socket


def log(*args, **kwargs):
    """
    用 log 代替 print
    """
    print('log', *args, **kwargs)


def route_index():
    """
    PATH  '/'
    """
    pass


def route_image():
    """
    PATH  '/doge.gif'
    """
    pass


def route_message():
    """
    PATH  '/messages'
    """
    pass


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    pass


def parsed_path(path):
    pass


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
                request.method = r.split()[0]
                # 把 body 放入 request 中
                request.body = r.split('\r\n\r\n', 1)[1]
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
