import sqlite3
from config import DEVICE_ID, UBICACION

DB_NAME = "access_control.db"


def conectar_db():

    return sqlite3.connect(DB_NAME)

# Crear tablas

def inicializar_db():

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS dispositivos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id TEXT UNIQUE NOT NULL,

            ubicacion TEXT,

            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP

        )

    """)

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS accesos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id TEXT,

            pin_ingresado TEXT,

            resultado TEXT,

            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP

        )

    """)

    conexion.commit()

    conexion.close()

# Registrar dispositivo

def registrar_dispositivo():

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("""

        INSERT OR IGNORE INTO dispositivos
        (device_id, ubicacion)

        VALUES (?, ?)

    """, (

        DEVICE_ID,
        UBICACION

    ))

    conexion.commit()

    conexion.close()

# Registrar acceso

def registrar_acceso(pin, resultado):

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("""

        INSERT INTO accesos
        (device_id, pin_ingresado, resultado)

        VALUES (?, ?, ?)

    """, (

        DEVICE_ID,
        pin,
        resultado

    ))

    conexion.commit()

    conexion.close()


# Obtener bitácora

def obtener_accesos():

    conexion = conectar_db()

    cursor = conexion.cursor()

    cursor.execute("""

        SELECT * FROM accesos
        ORDER BY fecha_hora DESC

    """)

    registros = cursor.fetchall()

    conexion.close()

    return registros