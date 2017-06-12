#!/usr/bin/env python3

# session 字典里 每个随机生成的'session_id' 对应一个 'username'
session = {}


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def template(filename, **kwargs):
    """
    读取 html 模板文件
    要转为 utf-8 编码
    原来 boby 里面的 replace 放到这里
    占位符当作参数传入
    """
    path = 'templates/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        t = f.read()
        for k, v in kwargs.items():
            t = t.replace('{{' + k + '}}', str(v))
        return t


def response_with_header(headers, status_code=200):
    # status_code 应该有个字典，有对应的描述
    header = 'HTTP/1.x {} OK\r\n'.format(status_code)
    #  \r\n 不放在 join 前面，保证每个 header 都换行
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(location):
    headers = {
        'Content-Type': 'text/html',
    }
    headers['Location'] = location
    header = response_with_header(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')
