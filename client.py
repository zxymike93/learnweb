#! python3

import socket

s = socket.socket()


def get(url):
    pars = parsed_url(url)
    protocol = pars[0]
    host = pars[1]
    port = pars[2]
    path = pars[3]
    
    s.connect((host, port))
    print("连接 url: ")

    ip, port = s.getsockname()
    print('本机的 ip 和 port {} {}'.format(ip, port))

    http_request = 'GET /{} {}/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, protocol, host)
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
    return('把'响应'转为 str 格式', response.decode('utf-8'))


def main():
    url = 'http://movie.douban.com/top250'
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()
