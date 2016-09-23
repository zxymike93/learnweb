import requests
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
        super(Movie, self).__init__()
        self.ranking = 0
        self.cover_url = ''
        self.name = ''
        self.staff = ''
        self.publish_info = ''
        self.rating = 0
        self.quote = ''
        self.number_of_comments = 0


def save(data):
    data = str(data)
    path = 'doubanTop250.txt'
    with open(path, 'a', encoding='utf-8') as f:
        f.write(data)


def add_quote(div):
    """
    有些电影没有 <p class="quote">
    豆瓣直接把它忽略了
    需要单独判断
    """
    if div.xpath('.//span[@class="inq"]'):
        quote = div.xpath('.//span[@class="inq"]')[0].text
    else:
        quote = ''
    return quote


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
    movie.quote = add_quote(div)
    infos = div.xpath('.//div[@class="bd"]/p/text()')
    movie.staff, movie.publish_info = [i.strip() for i in infos[:2]]
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    return movie


def movies_from_url(url):
    page = requests.get(url)
    root = html.fromstring(page.content)
    movie_divs = root.xpath('//div[@class="item"]')
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def main():
    url = 'https://movie.douban.com/top250?start='
    for i in range(10):
        u = url + str(i * 25)
        movies = movies_from_url(u)
        save(movies)
        print(movies)


if __name__ == '__main__':
    main()