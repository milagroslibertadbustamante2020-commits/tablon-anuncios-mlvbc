# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        return vista(*args, **kwargs)
    return envoltura
