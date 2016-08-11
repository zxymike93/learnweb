#! python3

def parsed_url(url):
    # split 第二个参数不能用 -1
    # 因为可能破坏完整路径
    # 注意：返回的列表的第二个元素为 ""
    elements = url.split('/', 3)

    # 分出来的所有可能如下：
    # ["'http:' or 'https'", "", "'g.cn:3000' or 'g.cn'", "'' or 'search'"]
    # 这个 list 的长度可能为 1, 2, 3, 4

    length = len(elements)
    # 第一层 if-loop 用 elements[0] == "xxx"
    # length 只能用作第二层
    # 因为 url 可能不包含 protocol

    if elements[0] == 'http:':
        # 两种可能
        # http://g.cn
        # http://g.cn/
        protocol = 'HTTP'
        host = elements[2]
        port = 80
        path = '/'        
    elif elements[0] == 'https:':
        # https://g.cn
        protocol = 'HTTPS'
        host = elements[2]
        port = 443
        path = '/'
    else:
        # g.cn
        # g.cn/
        # g.cn:3000
        # g.cn:3000/search
        protocol = 'HTTP'
        host = elements[0].split(':', 1)[0]
        port = elements[0].split(':', 1)[1]
        if len(elements) == 1:
            path = '/'
        else:
            path = '/' + elements[1]
    return tuple(protocol, host, port, path)
