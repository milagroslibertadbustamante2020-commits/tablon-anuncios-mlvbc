# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            session.clear()
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            flash('Bienvenida, ' + usuario.nombre + '.', 'success')
            return redirect(url_for('main.inicio'))
        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('auth.login'))
