import os
from flask import Flask, render_template, redirect, url_for, flash, session, g, current_app, request
from dotenv import load_dotenv
from flask_login import current_user
from datetime import datetime
import logging
from flask_wtf.csrf import CSRFProtect

# Importar extensiones
from extensions import login_manager, mysql, init_extensions, get_cursor, mail

# Importar configuración
from config import get_config

# Importar blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.productos import productos_bp
from routes.categorias import categorias_bp
from routes.reparaciones import reparaciones_bp
from routes.whatsapp import whatsapp_bp
from routes.tienda import tienda_bp
from routes.clientes import clientes_bp
from routes.admin import admin_bp
from routes.ventas import ventas_bp
from routes.empleados import empleados_bp
from routes.carrito import carrito_bp
from routes.notificaciones import notificaciones_bp
from routes.carousel import carousel_bp
from routes.pagos_pse import pagos_pse_bp

# Importar base de datos y modelos
import database as db
from models.models import crear_tablas, insertar_datos_iniciales, verificar_estructura_tablas, inicializar_tablas_reparaciones
from models.usuario import Usuario
import pymysql

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Crear la instancia de Flask
app = Flask(__name__)

# Cargar configuración desde config.py
app.config.from_object(get_config())

# Proteger formularios con CSRF
csrf = CSRFProtect(app)

# Inicializar extensiones
init_extensions(app)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(reparaciones_bp)
app.register_blueprint(whatsapp_bp)
app.register_blueprint(tienda_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(empleados_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(notificaciones_bp)
app.register_blueprint(carousel_bp)
app.register_blueprint(pagos_pse_bp)

# Inicializar base de datos si es necesario
with app.app_context():
    crear_tablas()
    insertar_datos_iniciales()
    verificar_estructura_tablas()
    inicializar_tablas_reparaciones()

# Flask necesita saber cuál es la app
if __name__ == '__main__':
    app.run(debug=True)
