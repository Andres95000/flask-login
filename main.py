from flask import request, make_response, redirect, render_template, session, url_for, flash
from flask_login import login_required, current_user

import unittest
from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_services import get_users, get_todos, put_todo, delete_todo, update_todo


app = create_app()

todos = ['Comprar cafe', 'Enviar solicitud de compra', 'Entregar video productor']

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests') # Los tests van hacer todo lo que encuentre en la carpeta "tests"
    unittest.TextTestRunner().run(tests) # Va correr todo lo que este en la carpeta "tests"

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error = error)

@app.errorhandler(500)
def not_found_server(error):
    return render_template('500.html', error = error)

@app.route('/')
def index():
    user_ip = request.remote_addr # Para obtener la ip del usuario

    response = make_response(redirect('/hello')) # response esta redireccionando a la ruta "hello"
    session['user_ip'] = user_ip # Estamos guardando la ip del usuario en las cookies, "session" estamos encriptando la ip del usuario

    return response

@app.route('/hello', methods = ['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip') # Estamos obteniendo las cookies del usuario guardadas en la funcion "index".
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    context = {
         'user_ip': user_ip,
         'todos': get_todos(user_id = username),
         'username': username,
         'todo_form': todo_form,
         'delete_form': delete_form,
         'update_form': update_form
    } # estamos guardando las variables en un diccionario para tener mas orden en el codigo, cuando pasemos como parametro en el "render_template".

    if todo_form.validate_on_submit():
        put_todo(user_id=username, descripcion = todo_form.descripcion.data)

        flash('Tu tarea se creo con exito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context) # Estamos renderizando el template "hello.html" y como segundo parametro el diccionario "**context", los ** son para expandir el diccionario y no tener que usar la extension Ejemplo:"context.user_ip" al llamar la variable en el template.

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for('hello'))