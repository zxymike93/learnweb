#! python3

import socket


def parsed_url(url):
    """
    分析 url 
    返回 protocol, host, port, path
    """
    pass


def socket_by_protocol(protocol):
    """
    根据 protocol 是 HTTP / HTTPS
    使用不同的 socket 初始化方式
    返回一个 socket 实例
    """
    pass


def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取（传输）的所有数据
    也就是 response
    """
    pass


def parsed_response(r):
    """
    把 response 解析出 status_code, headers, body
    status_code 是 int
    headers 是 dict
    body 是 str
    """
    pass


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
