# Sistema de Control de Acceso

Sistema de control de acceso mediante teclado numérico web, construido con Flask y diseñado para correr en una Raspberry Pi. Permite ingresar un PIN desde cualquier navegador en la red local, controla LEDs físicos como indicadores visuales y registra todos los intentos de acceso en una base de datos SQLite.

## Características

- Teclado numérico web con interfaz oscura responsive
- Validación de PIN configurable
- Control de LEDs verde (acceso autorizado) y rojo (acceso denegado) via GPIO
- Bitácora de accesos almacenada en SQLite
- Soporte para modo simulación cuando no hay hardware GPIO disponible (útil para desarrollo en PC)
- Actualización de estado en tiempo real sin recargar la página

## Estructura del proyecto

```
.
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración: Device ID, ubicación y PIN
├── db.py               # Módulo de base de datos (SQLite)
├── hardware.py         # Control de LEDs via GPIO (con modo simulación)
├── requirements.txt    # Dependencias Python
├── static/
│   ├── script.js       # Lógica del teclado en el cliente
│   └── style.css       # Estilos de la interfaz
└── templates/
    └── index.html      # Plantilla HTML del panel de acceso
```

## Requisitos

- Python 3.8 o superior
- Raspberry Pi con GPIO (opcional — funciona en modo simulación en cualquier PC)
- LEDs conectados a los pines BCM 17 (verde) y 27 (rojo) con sus resistencias

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

### 2. Crear y activar un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate       # Linux / macOS / Raspberry Pi OS
# venv\Scripts\activate        # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> Si se ejecuta en Raspberry Pi y se requiere control GPIO, instalar además:
> ```bash
> pip install RPi.GPIO
> ```

### 4. Configurar el sistema

Editar `config.py` con los valores del dispositivo:

```python
DEVICE_ID = "CASA-001"      # Identificador único del dispositivo
UBICACION = "Garaje Casa 1" # Descripción de la ubicación
PIN_CORRECTO = "1234"       # PIN de acceso (cambiar antes de usar)
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en `http://<ip-del-dispositivo>:5000` desde cualquier dispositivo en la misma red.

## Uso

1. Abrir el navegador y acceder a la dirección del servidor.
2. Ingresar el PIN usando el teclado en pantalla.
3. Presionar **OK** para validar.
   - **LED verde encendido** → acceso autorizado.
   - **LED rojo encendido** → acceso denegado.
4. El sistema se bloquea por 5 segundos mientras procesa el resultado y luego queda disponible para un nuevo intento.

## Modo simulación

Si `RPi.GPIO` no está instalado (por ejemplo, al desarrollar en una PC), el sistema inicia automáticamente en **modo simulación**. En este modo, el estado de los LEDs se imprime en la consola en lugar de activar el hardware físico. No es necesaria ninguna configuración adicional.

## Seguridad

> ⚠️ Este proyecto es un prototipo educativo. Antes de usarlo en un entorno real, considerar:
> - Cambiar el PIN por defecto en `config.py`.
> - No exponer el servidor directamente a internet sin autenticación adicional.
> - Usar HTTPS si el sistema se accede fuera de la red local.

