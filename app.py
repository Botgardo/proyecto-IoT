from flask import Flask, render_template, request, jsonify
import threading
import time

from config import PIN_CORRECTO

from hardware import (
    prender_led,
    apagar_led,
    LED_VERDE,
    LED_ROJO
)

from db import (
    inicializar_db,
    registrar_dispositivo,
    registrar_acceso,
    obtener_accesos
)

app = Flask(__name__)


# Estado del sistema
sistema_ocupado = False
mensaje_global = "Ingresa el PIN de acceso"


# Inicializar DB
inicializar_db()
registrar_dispositivo()

# Finalizar ciclo

def finalizar_ciclo(pin, segundos, mensaje_final):

    global sistema_ocupado
    global mensaje_global

    time.sleep(segundos)

    apagar_led(pin)

    sistema_ocupado = False
    mensaje_global = mensaje_final


@app.route("/")
def inicio():

    accesos = obtener_accesos()

    return render_template(
        "index.html",
        mensaje=mensaje_global,
        sistema_ocupado=sistema_ocupado,
        accesos=accesos
    )


@app.route("/validar", methods=["POST"])
def validar():

    global sistema_ocupado
    global mensaje_global

    if sistema_ocupado:

        return jsonify({
            "mensaje": "Sistema ocupado",
            "ocupado": True
        })
    
    pin = request.form["pin"]

    sistema_ocupado = True


    # Correcto
    if pin == PIN_CORRECTO:

        prender_led(LED_VERDE)

        mensaje_global = "Acceso autorizado"

        registrar_acceso(pin, "AUTORIZADO")

        threading.Thread(
            target=finalizar_ciclo,
            args=(
                LED_VERDE,
                5,
                "Ingresa el PIN"
            ),
            daemon=True
        ).start()


    # Incorrecto
    else:

        prender_led(LED_ROJO)

        mensaje_global = "Acceso denegado"

        registrar_acceso(pin, "DENEGADO")

        threading.Thread(
            target=finalizar_ciclo,
            args=(
                LED_ROJO,
                5,
                "Puede intentar nuevamente"
            ),
            daemon=True
        ).start()


    return jsonify({
        "mensaje": mensaje_global,
        "ocupado": sistema_ocupado
    })

@app.route("/estado")
def estado():

    return jsonify({
        "mensaje": mensaje_global,
        "ocupado": sistema_ocupado
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
