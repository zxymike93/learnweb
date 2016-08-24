#!/user/bin/env python3

class Message(object):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')

    def __repr__(self):
        return '{}: {}'.format(self.author, self.message)