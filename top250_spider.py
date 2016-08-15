#! python3

import socket
import ssl
import re


def log(*args, **kwargs):
    print(*args, **kwargs)


def parsed_url(url):
    """
    分析 url
    返回 protocol, host, port, path
    """
    # 分割出 protocol
    protocol = 'http'
    if url[:7] == 'http://':
        left = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        left = url.split('://')[1]
    else:
        left = url

    # 分割出 path
    # 分割出 host
    i = left.find('/')
    if i == -1:
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
    port = port_dict[protocol]
    # 有特别指明 port 则分割出 host, port
    if host.find(':') != -1:
        p = host.split(':')
        host = p[0]
        port = int(p[1])

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


def spider(body, page):
    """
    爬取函数
    """
    re_title = r'<span class="title">(.*?)</span>'
    re_rating = r'<span class="rating_num" property="v:average">(\d.\d)</span>'
    # re_votes = r'<span>('人评价'$)</span>'
    # re_quote = r'<span class="inq">(.*?)</span>'

    title = re.findall(re_title, body, re.S)
    rating = re.findall(re_rating, body, re.S)
    # votes = re.findall(re_votes, body, re.S)
    # quote = re.findall(re_quote, body, re.S)

    top = 0
    p = page * 25
    # 过滤大陆以外的片名
    for t in title:
        if t.find('&nbsp') == -1:
            log('Top{} 《{}》 {}分'.format(str(top + p + 1), t, rating[top]))
            top += 1


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
    url = 'http://movie.douban.com/top250?start='
    for page in range(10):
        u = url + str(page * 25)
        status_code, headers, body = get(u)
        # print(status_code, headers, body)
        spider(body, page)


def test_parsed_url():
    """
    parsed_url 函数很容易出错
    所以要有测试函数来检测其是否正确
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('g.cn', (http, host, 80, path)),
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/search', (http, host, 90, '/search')),
        ('https://g.cn', (https, host, 443, path)),
    ]
    for item in test_items:
        url, expected = item
        u = parsed_url(url)
        # assert 是一个语句 ‘断言’
        # 如果断言成功，条件成立，则通过测试，否则测试失败，终端程序报错
        e = "parsed_url Error, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
               'Content-Type: text/html\r\n' \
               'Location: https://movie.douban.com/top250\r\n' \
               'Content-Length: 178\r\n\r\n' \
               'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'


def test_get():
    """
    测试是否能正确处理 HTTP 和 HTTPS
    """
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    for u in urls:
        get(u)


def test():
    """
    用于测试的主函数
    """
    test_parsed_url()
    test_parsed_response()
    test_get()


if __name__ == '__main__':
    test()
    main()
