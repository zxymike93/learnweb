#! python3

import socket

host = '127.0.0.1'
port = 2000

s = socket.socket()

s.connect((host, port))
print("连接IP地址'127.0.0.1:2000'")

ip, port = s.getsockname()
print('本机的 ip 和 port {} {}'.format(ip, port))

http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
request = http_request.encode('utf-8')
s.send(request)
print('发送"请求"', request)

response = b''
while True:
    r = s.recv(1024)
    response += r
    if len(r) == 0:
      break
    # print('收到"响应"', response)
print('把'响应'转为 str 格式', response.decode('utf-8'))
