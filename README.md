# Sistema de Control de Acceso

Sistema de control de acceso mediante teclado numérico web, construido con Flask y diseñado para correr en una Raspberry Pi. Permite ingresar un PIN desde cualquier navegador en la red local, controla LEDs físicos como indicadores visuales y registra todos los intentos de acceso en una base de datos PostgreSQL centralizada en la nube.

## Características

- Teclado numérico web con interfaz oscura responsive
- Validación de PIN configurable por dispositivo
- Control de LEDs verde (acceso autorizado) y rojo (acceso denegado) via GPIO
- Bitácora de accesos centralizada en PostgreSQL (Railway)
- Soporte para múltiples dispositivos: cada uno se identifica con su propio `DEVICE_ID`
- Soporte para modo simulación cuando no hay hardware GPIO disponible (útil para desarrollo en PC)
- Actualización de estado en tiempo real sin recargar la página

## Estructura del proyecto

```
.
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración: Device ID, ubicación y PIN
├── db.py               # Módulo de base de datos (PostgreSQL)
├── hardware.py         # Control de LEDs via GPIO (con modo simulación)
├── requirements.txt    # Dependencias Python
├── .env.example        # Plantilla para variables de entorno
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
- Base de datos PostgreSQL (el proyecto usa Railway)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Botgardo/proyecto-IoT.git
cd proyecto-IoT
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

### 4. Configurar las variables de entorno

Copiar el archivo de ejemplo y agregar la URL de la base de datos:

```bash
cp .env.example .env
```

Editar `.env` con la URL de conexión a PostgreSQL:

```
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_db
```

> ⚠️ Nunca subas el archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

### 5. Configurar el dispositivo

Editar `config.py` con los valores únicos de este dispositivo:

```python
DEVICE_ID = "CASA-001"       # Identificador único — cambiarlo en cada dispositivo
UBICACION = "Garaje Casa 1"  # Descripción de la ubicación
PIN_CORRECTO = "1234"        # PIN de acceso (cambiar antes de usar)
```

> Cada dispositivo debe tener un `DEVICE_ID` distinto para que los registros queden correctamente identificados en la base de datos central.

### 6. Ejecutar la aplicación

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

## Base de datos centralizada

Todos los dispositivos que compartan la misma `DATABASE_URL` en su `.env` escribirán sus registros en la misma base de datos PostgreSQL. Esto permite ver la bitácora completa de todos los puntos de acceso desde un solo lugar, identificando cada registro por su `DEVICE_ID`.

## Modo simulación

Si `RPi.GPIO` no está instalado (por ejemplo, al desarrollar en una PC), el sistema inicia automáticamente en **modo simulación**. En este modo, el estado de los LEDs se imprime en la consola en lugar de activar el hardware físico. No es necesaria ninguna configuración adicional.

## Seguridad

> ⚠️ Este proyecto es un prototipo educativo. Antes de usarlo en un entorno real, considerar:
>
> - Cambiar el PIN por defecto en `config.py`.
> - No exponer el servidor directamente a internet sin autenticación adicional.
> - Usar HTTPS si el sistema se accede fuera de la red local.
> - No compartir la `DATABASE_URL` con personas no autorizadas.