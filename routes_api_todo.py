from models import Todo
from response import response_with_header, template
from utils import log


def route_index():
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_header(headers)
    todos = Todo.all()
    def todo_tag(todo):
        status = todo.status()
        return '<p class="{}">{} {} @ {}<a href="/todo/complete?id={}">完成</a></p>'.format(
            status,
            todo.id,
            todo.content,
            todo.created_time,
            todo.id,
        )
    todo_html = '\n'.join([todo_tag(todo) for todo in todos])
    body = template('todo_index.html', todos=todo_html)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_add(request):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_header(headers)
    form = request.form()
    t = Todo(form)
    log('add todo', t)
    t.save()
    # 返回的不是一个完整的 html 的 body，只是要插入的数据
    body = t.json_str()
    log('add body', body)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_complete(request):
    headers = {
        'Content-Type': 'text/html',
    }
    id = int(request.query.get('id', -1))
    t = Todo.find(id)
    t.toggleComplete()
    t.save()
    return redirect('/todo')


route_dict = {
    '/api/todo': route_index,
    '/api/todo/add': route_add,
}