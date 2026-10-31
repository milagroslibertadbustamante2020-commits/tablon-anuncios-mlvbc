# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models import Categoria
from app.utils import login_required

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias', template_folder='templates')


@categorias_bp.route('/')
@login_required
def lista():
    q = request.args.get('q', '').strip()
    consulta = Categoria.query
    if q:
        consulta = consulta.filter(Categoria.nombre.ilike('%' + q + '%'))
    categorias = consulta.order_by(Categoria.id).all()
    return render_template('categorias/lista.html', categorias=categorias, q=q)


@categorias_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        descripcion = request.form['descripcion'].strip()
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
        elif Categoria.query.filter_by(nombre=nombre).first():
            flash('Ya existe una categoría con ese nombre.', 'danger')
        else:
            db.session.add(Categoria(nombre=nombre, descripcion=descripcion))
            db.session.commit()
            flash('Categoría registrada correctamente.', 'success')
            return redirect(url_for('categorias.lista'))
    return render_template('categorias/form.html', categoria=None)


@categorias_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    categoria = db.get_or_404(Categoria, id)
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        descripcion = request.form['descripcion'].strip()
        otra = Categoria.query.filter_by(nombre=nombre).first()
        if not nombre:
            flash('El nombre es obligatorio.', 'danger')
        elif otra and otra.id != categoria.id:
            flash('Ya existe otra categoría con ese nombre.', 'danger')
        else:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            db.session.commit()
            flash('Categoría actualizada correctamente.', 'success')
            return redirect(url_for('categorias.lista'))
    return render_template('categorias/form.html', categoria=categoria)


@categorias_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar(id):
    categoria = db.get_or_404(Categoria, id)
    if categoria.anuncios:
        flash('No se puede eliminar: la categoría tiene anuncios asociados.', 'danger')
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada correctamente.', 'success')
    return redirect(url_for('categorias.lista'))
