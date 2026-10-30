# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import Usuario
from app.utils import login_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios', template_folder='templates')


@usuarios_bp.route('/')
@login_required
def lista():
    q = request.args.get('q', '').strip()
    consulta = Usuario.query
    if q:
        consulta = consulta.filter(db.or_(Usuario.nombre.ilike('%' + q + '%'),
                                          Usuario.email.ilike('%' + q + '%')))
    usuarios = consulta.order_by(Usuario.id).all()
    return render_template('usuarios/lista.html', usuarios=usuarios, q=q)


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
        elif Usuario.query.filter_by(email=email).first():
            flash('Ya existe un usuario con ese correo.', 'danger')
        else:
            usuario = Usuario(nombre=nombre, email=email)
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario registrado correctamente.', 'success')
            return redirect(url_for('usuarios.lista'))
    return render_template('usuarios/form.html', usuario=None)


@usuarios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    usuario = db.get_or_404(Usuario, id)
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        otro = Usuario.query.filter_by(email=email).first()
        if not nombre or not email:
            flash('Nombre y correo son obligatorios.', 'danger')
        elif otro and otro.id != usuario.id:
            flash('Ese correo ya pertenece a otro usuario.', 'danger')
        else:
            usuario.nombre = nombre
            usuario.email = email
            if password:
                usuario.set_password(password)
            db.session.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('usuarios.lista'))
    return render_template('usuarios/form.html', usuario=usuario)


@usuarios_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    usuario = db.get_or_404(Usuario, id)
    if usuario.id == session.get('usuario_id'):
        flash('No puedes eliminar tu propio usuario.', 'danger')
    elif usuario.anuncios:
        flash('No se puede eliminar: el usuario tiene anuncios asociados.', 'danger')
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('usuarios.lista'))
