#! python3

import socket
import ssl
# import re
# 用 lxml库 里的 html类 来对 body 做处理
from lxml import html


class Model(object):
    """
    log(movies) 会调用 str(movies)
    首先会查找 m.__str__() 其次是 m.__repr__()
    如果 Movie类 没有这两个方法
    就会一直往上在它的父类里面寻找这两个方法
    """
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (u'{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{}:\n  {}\n>'.format(class_name, u'\n  '.join(properties))
        return r


class Movie(Model):
    def __init__(self):
        self.ranking = 0
        self.cover_url = ''
        self.name = ''
        self.staff = ''
        self.publish_info = ''
        self.rating = 0
        self.quote = ''
        self.number_of_comments = 0


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


def get(url):
    """
    发送 GET请求 并得到 响应
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


def movie_from_div(div):
    """
    . 表示从当前路径 div 下面查找
    text 是 开始/结束标签 之间的信息
    """
    movie = Movie()
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@src')
    names = div.xpath('.//span[@class="title"]/text()')
    movie.name = ''.join(names)
    movie.rating = div.xpath('.//span[@class="rating_num"]')[0].text
    movie.quote = div.xpath('.//span[@class="inq"]')[0].text
    infos = div.xpath('.//div[@class="bd"]/p/text()')
    movie.staff, movie.publish_info = [i.strip() for i in infos[:2]]
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    return movie


def movie_from_url(url):
    # status_code, headers 用 _ 替换掉
    status_code, headers, page = get(url)
    # 把 page 转换成 html类，它的 xpath方法 可以查找数据
    root = html.fromstring(page)
    # @ 表示属性
    # // 表示从 html 根源处开始查找所有
    # class="item" 每页有25条，即每页25部电影
    movie_divs = root.xpath('//div[@class="item"]')
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def main():
    url = 'http://movie.douban.com/top250'
    movies = movie_from_url(url)
    log('Names', names)
    log('movies', movies[0])
    # download_covers(movies)


if __name__ == '__main__':
    main()
