import psycopg2
import os
from config import DEVICE_ID, UBICACION

DATABASE_URL = os.getenv("DATABASE_URL")


def conectar_db():

    return psycopg2.connect(DATABASE_URL)


# Crear tablas
def inicializar_db():

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispositivos (
            id SERIAL PRIMARY KEY,
            device_id TEXT UNIQUE NOT NULL,
            ubicacion TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accesos (
            id SERIAL PRIMARY KEY,
            device_id TEXT,
            pin_ingresado TEXT,
            resultado TEXT,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexion.commit()
    conexion.close()


# Registrar dispositivo
def registrar_dispositivo():

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO dispositivos (device_id, ubicacion)
        VALUES (%s, %s)
        ON CONFLICT (device_id) DO NOTHING
    """, (DEVICE_ID, UBICACION))

    conexion.commit()
    conexion.close()


# Registrar acceso
def registrar_acceso(pin, resultado):

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO accesos (device_id, pin_ingresado, resultado)
        VALUES (%s, %s, %s)
    """, (DEVICE_ID, pin, resultado))

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