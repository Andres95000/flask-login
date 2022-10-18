from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', [InputRequired('Por favor ingrese su nombre.')])
    password = PasswordField('Password', [InputRequired('Por favor ingrese una contraseña.')])
    submit = SubmitField('Enviar')

class TodoForm(FlaskForm):
    descripcion = StringField('Descripcion', validators=[InputRequired('Ingrese una descripcion')])
    submit = SubmitField('Crear')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')