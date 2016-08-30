#!/usr/bin/env python3

from models import User, Weibo

from response import session, error, template, redirect, response_with_header

from utils import log


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, 'guest')
    return username


def route_weibo_index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_header(headers)
    user_id = request.query.get('user_id', -1)
    user_id = int(user_id)
    user = User.find(user_id)
    if user is None:
        return error(request)
    # 找到 user 发布的所有 weibo
    weibos = Weibo.find_all(user_id=user.id)
    # 手动处理 weibos 这个 list
    # 把每个 weibo 以 <p> 的形式展现在页面
    def weibo_tag(weibo):
        return '<p>{} from {}@{} <a href="/weibo/delete?id={}">删除</a></p>'.format(
            weibo.content,
            user.username,
            weibo.created_time,
            weibo.id,
        )
    # 用 join() 返回 str
    weibos = ''.join([weibo_tag(w) for w in weibos])
    body = template('weibo_index.html', weibos=weibos)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_weibo_new(request):
    """
    返回微博表单的路由
    """
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    header = response_with_header(headers)
    log('Debug username', username)
    user = User.find_by(username=username)
    body = template('weibo_new.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_weibo_add(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    log('username', username)
    header = response_with_header(headers)
    # log('add header', header)
    user = User.find_by(username=username)
    # log('add user', user)
    # 创建微博
    form = request.form()
    # log('form', form)
    w = Weibo(form)
    # log('w', w)
    w.user_id = user.id
    # log('user_id', w.user_id)
    w.save()
    # log('save', w)
    return redirect('/weibo?user_id={}'.format(user.id))


def route_weibo_delete(request):
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    header = response_with_header(headers)
    user = User.find_by(username=username)
    # 删除微博
    weibo_id = request.query.get('id', None)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    w.delete()
    return redirect('/weibo?user_id={}'.format(user.id))


def login_required(route_function):
    """
    用来验证用户身份
    """
    def func(request):
        username = current_user(request)
        log('登录验证', username)
        if username == 'guest':
            return redirect('/login')
        return route_function(request)
    return func


route_dict = {
    '/weibo': route_weibo_index,
    '/weibo/new': login_required(route_weibo_new),
    '/weibo/add': login_required(route_weibo_add),
    '/weibo/delete': login_required(route_weibo_delete),
}