#!/user/bin/env python3

class User(object):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '<{}\n{}>'.format(class_name, s)

    def validate_login(self):
        return self.username == 'mike' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 3 and len(self.password) >3


class Message(object):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')

    def __repr__(self):
        return '{}: {}'.format(self.author, self.message)