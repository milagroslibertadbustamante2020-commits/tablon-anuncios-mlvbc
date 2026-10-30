# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Blueprint, render_template
from app.models import Usuario, Categoria, Anuncio
from app.utils import login_required

main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
@login_required
def inicio():
    totales = {
        'usuarios': Usuario.query.count(),
        'categorias': Categoria.query.count(),
        'anuncios': Anuncio.query.count(),
    }
    return render_template('main/inicio.html', totales=totales)
