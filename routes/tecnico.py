from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import mysql
import MySQLdb
from utils.decorators import tecnico_required
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

# Blueprint
tecnico_bp = Blueprint('tecnico', __name__, url_prefix='/tecnico')

@tecnico_bp.route('/dashboard')
@login_required
@tecnico_required
def dashboard():
    """Dashboard del técnico"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        # Obtener estadísticas
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN estado = 'PENDIENTE' THEN 1 END) as pendientes,
                COUNT(CASE WHEN estado = 'EN_PROGRESO' THEN 1 END) as en_progreso,
                COUNT(CASE WHEN estado = 'COMPLETADO' THEN 1 END) as completadas
            FROM reparaciones 
            WHERE tecnico_id = %s
        """, (current_user.id,))
        
        stats = cursor.fetchone()
        return render_template('tecnico/dashboard/index.html', stats=stats)
    finally:
        cursor.close()

@tecnico_bp.route('/reparaciones/pendientes')
@login_required
@tecnico_required
def pendientes():
    """Reparaciones pendientes del técnico"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT r.*, c.nombre as cliente_nombre
            FROM reparaciones r
            LEFT JOIN clientes c ON r.cliente_id = c.id
            WHERE r.tecnico_id = %s AND r.estado = 'PENDIENTE'
            ORDER BY r.fecha_recepcion ASC
        """, (current_user.id,))
        
        reparaciones = cursor.fetchall()
        return render_template('tecnico/reparaciones/pendientes.html', 
                             reparaciones=reparaciones)
    finally:
        cursor.close()

@tecnico_bp.route('/reparaciones/en-progreso')
@login_required
@tecnico_required
def en_progreso():
    """Reparaciones en progreso del técnico"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT r.*, c.nombre as cliente_nombre
            FROM reparaciones r
            LEFT JOIN clientes c ON r.cliente_id = c.id
            WHERE r.tecnico_id = %s AND r.estado = 'EN_PROGRESO'
            ORDER BY r.fecha_actualizacion DESC
        """, (current_user.id,))
        
        reparaciones = cursor.fetchall()
        return render_template('tecnico/reparaciones/en_progreso.html', 
                             reparaciones=reparaciones)
    finally:
        cursor.close()