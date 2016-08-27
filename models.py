#!/user/bin/env python3
#-*- coding: utf-8 -*-

import json

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
        path = '{}.txt'.format(class_name)
        return path

    @classmethod
    def all(cls):
        """
        load 出来的是该 cls 所有实例的所有数据
        列表生成式 把 数据 转化为 所有的实例
        """
        path = cls.db_path()
        data = load(path)
        all_ins = [cls(i) for i in data]
        return all_ins

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '>{}\n{}<\n'.format(class_name, s)

    def save(self):
        all_ins = self.all()
        all_ins.append(self)
        l = [i.__dict__ for i in all_ins]
        path = self.db_path()
        save(l, path)


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # 为了测试 Set-Cookie 让所有登录的用户都通过验证
        return True


    def validate_register(self):
        return len(self.username) > 3 and len(self.password) >3


class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')