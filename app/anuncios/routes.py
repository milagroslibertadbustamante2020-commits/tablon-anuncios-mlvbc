# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models import Anuncio, Categoria, Usuario
from app.utils import login_required

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios', template_folder='templates')


@anuncios_bp.route('/')
@login_required
def lista():
    q = request.args.get('q', '').strip()
    categoria_id = request.args.get('categoria_id', type=int)
    consulta = Anuncio.query
    if q:
        consulta = consulta.filter(db.or_(Anuncio.titulo.ilike('%' + q + '%'),
                                          Anuncio.contenido.ilike('%' + q + '%')))
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)
    anuncios = consulta.order_by(Anuncio.fecha.desc()).all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template('anuncios/lista.html', anuncios=anuncios, categorias=categorias,
                           q=q, categoria_id=categoria_id)


@anuncios_bp.route('/<int:id>')
@login_required
def detalle(id):
    anuncio = db.get_or_404(Anuncio, id)
    return render_template('anuncios/detalle.html', anuncio=anuncio)


@anuncios_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    if not categorias:
        flash('Primero registra al menos una categoría.', 'warning')
        return redirect(url_for('categorias.nueva'))
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        contenido = request.form['contenido'].strip()
        categoria_id = request.form.get('categoria_id', type=int)
        usuario_id = request.form.get('usuario_id', type=int)
        if not titulo or not contenido or not categoria_id or not usuario_id:
            flash('Todos los campos son obligatorios.', 'danger')
        else:
            db.session.add(Anuncio(titulo=titulo, contenido=contenido,
                                   categoria_id=categoria_id, usuario_id=usuario_id))
            db.session.commit()
            flash('Anuncio registrado correctamente.', 'success')
            return redirect(url_for('anuncios.lista'))
    return render_template('anuncios/form.html', anuncio=None, categorias=categorias,
                           usuarios=usuarios, usuario_actual=session.get('usuario_id'))


@anuncios_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    anuncio = db.get_or_404(Anuncio, id)
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        contenido = request.form['contenido'].strip()
        categoria_id = request.form.get('categoria_id', type=int)
        usuario_id = request.form.get('usuario_id', type=int)
        if not titulo or not contenido or not categoria_id or not usuario_id:
            flash('Todos los campos son obligatorios.', 'danger')
        else:
            anuncio.titulo = titulo
            anuncio.contenido = contenido
            anuncio.categoria_id = categoria_id
            anuncio.usuario_id = usuario_id
            db.session.commit()
            flash('Anuncio actualizado correctamente.', 'success')
            return redirect(url_for('anuncios.lista'))
    return render_template('anuncios/form.html', anuncio=anuncio, categorias=categorias,
                           usuarios=usuarios, usuario_actual=anuncio.usuario_id)


@anuncios_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    anuncio = db.get_or_404(Anuncio, id)
    db.session.delete(anuncio)
    db.session.commit()
    flash('Anuncio eliminado correctamente.', 'success')
    return redirect(url_for('anuncios.lista'))
