from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from database import db
from models import User
from . import auth
from .forms import LoginForm, RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Validamos el formulario y registramos al usuario si todo es correcto
    if form.validate_on_submit():
        # Validamos que el usuario no exista ya en la base de datos
        if User.query.filter_by(username=form.username.data).first():
            # Si el usuario ya existe, mostramos un mensaje de error y redirigimos al formulario de registro
            flash('Ese nombre de usuario ya está registrado.')
            # Redirigimos al formulario de registro para que el usuario intente con otro nombre
            return redirect(url_for('auth.register'))
            
        # Creamos y guardamos al usuario (la contraseña se encripta por el modelo)
        nuevo_usuario = User(username=form.username.data, password=form.password.data)
        db.session.add(nuevo_usuario)
        db.session.commit()
        # Mostramos un mensaje de éxito y redirigimos al formulario de inicio de sesión        
        flash('Registro exitoso. Ya puedes iniciar sesión.')
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Validamos usando el método verify_password que creamos en models.py
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Has iniciado sesión correctamente')
            return redirect(url_for('profile'))
        else:
            flash('Credenciales inválidas')
    return render_template("login.html", form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))