import time

try:
    import RPi.GPIO as GPIO
    RPI = True
    print("Modo Raspberry Pi")

except ImportError:
    RPI = False
    print("Modo simulación")


LED_VERDE = 17
LED_ROJO = 27


if RPI:

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(LED_VERDE, GPIO.OUT)
    GPIO.setup(LED_ROJO, GPIO.OUT)

# Encender LED

def prender_led(pin):

    if RPI:

        GPIO.output(pin, True)

    else:

        print(f"[SIMULACION] LED {pin} ENCENDIDO")


# Apagar LED

def apagar_led(pin):

    if RPI:

        GPIO.output(pin, False)

    else:

        print(f"[SIMULACION] LED {pin} APAGADO")