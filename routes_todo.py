#! /usr/bin/env python3

"""
自己写的野鸡 todo-list
只有一个主页面
    可以在表单里面添加 todo
    可以改变任务状态 待办/完成
    可以删除任务
"""

from models import Todo

from response import template, redirect, response_with_header

from utils import log


def route_todo_index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_header(headers)
    todos = Todo.all()
    log('todos', todos)

    def todo_tag(t):
        status = t.status()
        tag = ('<p class="{}">{}, {}@{} '
               '<a href="/todo/delete?id={}">删除</a> '
               '<a href="/todo/complete?id={}">完成</a></p>')
        return tag.format(
            status,
            t.id,
            t.content,
            t.created_time,
            t.id,
            t.id,
        )
    todo_html = ''.join([todo_tag(t) for t in todos])
    body = template('todo_index.html', todos=todo_html)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_todo_add(request):
    form = request.form()
    t = Todo(form)
    t.save()
    return redirect('/todo')


def route_todo_delete(request):
    todo_id = request.query.get('id', None)
    todo_id = int(todo_id)
    t = Todo.find(todo_id)
    t.delete()
    return redirect('/todo')


def route_todo_complete(request):
    todo_id = request.query.get('id', None)
    todo_id = int(todo_id)
    t = Todo.find(todo_id)
    t.toggleComplete()
    t.save()
    return redirect('/todo')


route_dict = {
    '/todo': route_todo_index,
    '/todo/add': route_todo_add,
    '/todo/delete': route_todo_delete,
    '/todo/complete': route_todo_complete,
}
