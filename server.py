#! python3

import socket

host = ''
port = 2000

s = socket.socket()

s.bind((host, port))

while True:
    # listen() 开始监听
    s.listen(7)
    
    # accept() 接收来自 client 的连接
    connection, address = s.accept()
    
    request = connection.recv(1024)
    print('接收来自 ip {} 的 "请求"\n{}'.format(address, request.decode('utf-8')))
    
    response = b'<h1>Hello World!</h1>'
    connection.sendall(response)
    print('向 client 发送"响应"', response）
    
    connection.close()
    print('关闭连接')
