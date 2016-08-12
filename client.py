#! python3

import socket
import ssl


def parsed_url(url):
    """
    分析 url 
    返回 protocol, host, port, path
    """
    # 分割出 protocol
    protocol = 'http'
    if url[:7] == 'http://':
        left = url.split('://')[1]
    elif url[:8] == 'https':
        protocol = 'https'
        left = url.split('://')[1]
    else:
        left = url
    
    # 分割出 path
    # 分割出 host
    if left.find('/') == -1:
        host = left
        path = '/'
    else:
        host = left[:i]
        path = left[i:]
    
    # http 请求的默认 port=80
    # https 请求的默认 port=443
    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[procotol]
    # 有特别指明 port 则分割出 host, port
    if host.find(':') != -1:
        host = host.split(':')[0]
        port = int(host.split(':')[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据 protocol 是 HTTP / HTTPS
    使用不同的 socket 初始化方式
    返回一个 socket 实例
    """
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
    else:
        s = socket.socket()
    return s


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取（传输）的所有数据
    也就是 response
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) == 0:
            break
    return response


def parsed_response(r):
    """
    把 response 解析出 status_code, headers, body
    status_code 是 int
    headers 是 dict
    body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = int(h[0].split()[1])
    
    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    
    return status_code, headers, body


# 把上面复杂的逻辑全部封装成函数
def get(url):
    """
    发送 GET请求 并返回 响应
    包含 状态码 / headers / body
    """
    # 分析出 url 的 protocol, host, port, path
    protocol, host, port, path = parsed_url(url)
    
    # 创建 socket 实例
    # 建立连接
    s = socket_by_protocol(protocol)
    s.connect((host, port))
    
    # request 以 utf-8 编码发送
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))
    
    # 接收 response 并解码为 str
    response = response_by_socket(s)
    r = response.decode(encoding)
    
    # 如果 status_code 是301
    # 生成一个重定向
    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)
    
    return status_code, headers, body


def main():
    url = 'http://movie.douban.com/top250'
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()
