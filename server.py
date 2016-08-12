#! python3

import socket


def log(*args, **kwargs):
    """
    用 log 代替 print
    """
    pass


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    pass


def response_for_path(path):
    pass


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
            r = connection.recv(1024)
            r = r.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, request))
            try:
                # 
                # 
                path = r.split()[1]
                # 
                request.method = r.split()[0]
                # 
                request.body = r.split('\r\n\r\n', 1)[1]
                # 
                response = resoponse_for_path(path)
                # 
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
