# Cryptography 3CM17
## Practica Control de Acceso

Practica enfocada en registrar un correo y una contraseña usando el cifrado MD5 con Python. Guardar la contraseña cifrada en la base de datos y con ello hacer un login donde se pueda validar el acceso comparando los cifrados.

Se creó un HTML para ver los datos registrados, lo puedes ver en:

**table.html**

Puedes acceder a la vista y funcionamiento de este proyecto en: https://cryp-log.herokuapp.com/ - [Github](https://cryp-log.herokuapp.com/) 

### Descargar proyecto con Git:

* Crear una carpeta en tu computadora para clonar el proyecto
* Abrir una consola en la ubicación de esa carpeta
* Ejecutar el siguiente comando:
    - git clone https://github.com/ManuOSMx/crypto-login.git

### Instalar paquetes Python:

* pip install flask
* pip install Flask-Mail
* pip install psycopg2

### Crear la base de datos en PostgreSQL:

El script necesario para crear la base de datos se encuentra en:

data/schedule.sql

Posteriormente cambia las credenciales para acceder a tu base de datos en App.py

### Correr el programa:

* python App.py

### Usar entorno virtual para subir a Heroku:

Opcional: Te recomiendo renombrar la carpeta donde viene el proyecto a "**src**". 

* Ramificación de Carpetas Antes:
    - Carpeta Origen
        - **crypto-login**
            - proyecto
* Ramificación de Carpetas Después:
    - Carpeta Origen
        - **src**
            - proyecto
        
Dentro de la carpeta Origen:

* Instalar virtualenv:
    - pip install virtualenv
* Crear el entorno virtual
    - python -m venv venv

* Ramificación de Carpetas Después:
    - Carpeta Origen
        - src
            - proyecto
        - **venv**

Instalar todos los programas que usaste en el entorno virtual y posteriormente mandarlos al archivo requirements:

Ruta env: **cd venv/Scripts**

Instalas los paquetes necesarios y los mandas a src/requirements.txt:

* Un paquete necesario es: **pip install gunicorn**
* Mandar a requirements.txt:
    - **pip freeze > ../../src/requirements.txt**

## Importante

El mandar correos no funciona en Heroku pero si de manera local. Debido a que Flask-Mail no tiene como tal un plugin en Heroku. Como alternativa podrías usar Mailgun ya que este si tiene soporte en Heroku al momento de desplegar.