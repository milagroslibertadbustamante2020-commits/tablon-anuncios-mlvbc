-- Base de datos: bd_anuncios (SQLite)
-- Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
-- Script equivalente a las tablas que crea SQLAlchemy con db.create_all()

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro DATETIME
);

CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(60) NOT NULL UNIQUE,
    descripcion VARCHAR(200)
);

CREATE TABLE anuncios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(150) NOT NULL,
    contenido TEXT NOT NULL,
    fecha DATETIME,
    usuario_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
);
