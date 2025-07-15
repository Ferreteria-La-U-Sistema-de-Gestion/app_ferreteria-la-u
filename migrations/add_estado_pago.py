from database import get_db_connection

def run_migration():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Crear tabla de clientes si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            direccion TEXT,
            telefono VARCHAR(20),
            activo BOOLEAN DEFAULT TRUE,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultima_compra TIMESTAMP NULL,
            notas TEXT
        )
        """)
        
        # Agregar campo estado_pago a la tabla ventas si no existe
        cursor.execute("""
        ALTER TABLE ventas
        ADD COLUMN IF NOT EXISTS estado_pago VARCHAR(20) DEFAULT 'pendiente'
        """)
        
        conn.commit()
        print('Migración completada: Tabla clientes actualizada y campo estado_pago agregado a ventas')
        
    except Exception as e:
        print(f"Error en la migración: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()