#!/user/bin/env python3
#-*- coding: utf-8 -*-

import json
import time

from utils import log


def save(data, path):
    """
    data 本身是 dict / list
    用 json.dumps() 转为 str -- 序列化
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    """
    path 指定的文件是序列化后的 data
    用 json.loads() 反序列化
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        """
        cls 是调用 all方法 的类
        根据类名，命名一个文件来存储数据
        """
        class_name = cls.__name__
        path = 'db/{}.txt'.format(class_name)
        return path

    @classmethod
    def load(cls, d):
        """
        从保存的字典中生成对象
        setattr(m, k, v) 相当于 m[k]=v
        """
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        load 出来的是该 cls 所有实例的所有数据
        列表生成式 把 数据 转化为 所有的实例
        """
        path = cls.db_path()
        data = load(path)
        all_ins = [cls.load(i) for i in data]
        return all_ins

    @classmethod
    def find_all(cls, **kwargs):
        """
        """
        k, v = '', ''
        for key, val in kwargs.items():
            k, v = key, val
        all = cls.all()
        models = []
        for m in all:
            if v == m.__dict__[k]:
                models.append(m)
        return models

    @classmethod
    def find_by(cls, **kwargs):
        """
        find_by 通过用户的某项信息查找匹配该信息的所有用户
        """
        k, v = '', ''
        for key, val in kwargs.items():
            k, v = key, val
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        # 左边的 id 是 find_by方法 **kwargs 里面的 key
        # 右边的 id 是传入这个 find方法 的参数
        return cls.find_by(id=id)

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '>{}\n{}<\n'.format(class_name, s)

    def save(self):
        """
        route_register 的 validate 中调用
        """
        # 初始化所有的用户实例
        all_ins = self.all()
        # log('DEBUG-save-all_ins', all_ins)
        # 如果该注册的用户还没有 id ，即新用户
        if self.id is None:
            # 如果是空 list，说明“数据库”还没有元素
            if len(all_ins) == 0:
                # 第一个用户 id 设为 1
                self.id = 1
            # 否则，已存在元素
            else:
                # 新元素的 id 设为最后一个
                self.id = all_ins[-1].id + 1
            # 新元素插入“数据库”中
            all_ins.append(self)
        # 否则，元素已经有对应的 id 了
        else:
            index = -1
            # 遍历出 每个索引 和 每个实例
            for i, ins in enumerate(all_ins):
                # 找到该实例对应的 id
                if ins.id == self.id:
                    # 得到该用户实例对应的 index
                    index = i
                    break
            #
            all_ins[index] = self
        l = [i.__dict__ for i in all_ins]
        path = self.db_path()
        # 写进“数据库”中
        save(l, path)

    def delete(self):
        models = self.all()
        index = -1
        for i, m in enumerate(models):
            if self.id == m.id:
                index = i
                break
        del models[index]
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def json_str(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
        usr = User.find_by(username=self.username)
        if usr is not None and usr.password == self.password:
            return True

    def validate_register(self):
        return len(self.username) > 3 and len(self.password) > 3


class Message(Model):
    def __init__(self, form):
        self.id = None
        self.author = form.get('author', '')
        self.message = form.get('message', '')


class Weibo(Model):
    def __init__(self, form):
        # 每条微博有一个独立的 id
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.created_time = int(time.time())
        # user_id 用来关联 用户 / 他的微博
        self.user_id = form.get('user_id', None)


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.created_time = int(time.time())
        self.content = form.get('content', '')
        self.complete = False

    def toggleComplete(self):
        self.complete = not self.complete

    def status(self):
        return 'status-done' if self.complete else 'status-active'




def test_weibo():
    w = Weibo({})
    log(w.id, w.content, w.created_time)


def test():
    test_weibo()


if __name__ == '__main__':
    test()