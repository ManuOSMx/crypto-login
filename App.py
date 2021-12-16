from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.wrappers import Request
from flask_mail import Mail, Message
import psycopg2
import hashlib

app = Flask(__name__)

# Build localhost and port Ex. 000.0.0.0:3000
port_lh = 3000
localhost = '127.0.0.1' + ':' + str(port_lh)

# Config Mail in Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Config Heroku Postgress
# Credentials DB
try:
    connection = psycopg2.connect(
        host='localhost',
        user='userDB',
        password='PasswordDB',
        database='NameDB'
    )
    print("Conexion Exitosa")
except Exception as ex:
    print(ex)

# Session
app.secret_key = 'mysecretkey'

# Routes
@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/register')
def Register():
    return render_template('register.html')


@app.route('/restore')
def Restore():
    return render_template('restore.html')


@app.route('/restore-pass')
def RestorePass():
    return render_template('restore-pass.html')


@app.route('/thanks')
def Thanks():
    return render_template('thanks.html')


@app.route('/table')
def Table():
    cur = connection.cursor()
    cur.execute('SELECT * FROM users ORDER BY id ASC')
    data = cur.fetchall()
    print("DATOS TABLA")
    print(data)
    return render_template('table.html', users=data)


# Actions
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if len(email) == 0 | len(password) == 0:
            return redirect(url_for('Index'))
        else:
            # Agregar aquí el algoritmo de cifrado
            textUtf8 = password.encode("utf-8")
            hash = hashlib.md5(textUtf8)
            cipher = hash.hexdigest()

            cur = connection.cursor()
            cur.execute('SELECT * FROM users WHERE email = %s',
                        (email,))
            data = cur.fetchone()
            cur.close()

            if len(data) > 0:
                print("Usuario encontrado")

                # Verifica si la clave cifrada se encuentra en la base de datos
                if cipher == data[2]:
                    session["email"] = data[1]
                    print("Contraseña correcta")
                    return redirect(url_for('Thanks'))
                else:
                    flash('Contraseña incorrecta')
                    return redirect(url_for('Index'))
            else:
                print("Usuario no encontrado")

            # Validar si las contraseñas son iguales

            # Mandamos mensaje de confirmado
            print("DATOS INDEX")
            print(data)

            return redirect(url_for('Index'))


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        passwordConf = request.form['passwordConf']

        cur = connection.cursor()
        # Verificar si el correo ya esta registrado y despues meter el if
        if len(password) != 8:
            flash("La contraseña debe de ser 8 digitos")
            return Edit_user(id)
        else:
            # Validar si las contraseñas son iguales
            if (password == passwordConf):
                # Algoritmo de cifrado
                textUtf8 = password.encode("utf-8")
                hash = hashlib.md5(textUtf8)
                cipher = hash.hexdigest()

                # Se agrega a la base de datos el email y el password cifrado
                cur.execute('INSERT INTO users (email,pass,pass_ext) VALUES (%s,%s,%s)',
                            (email, cipher, passwordConf))
                connection.commit()
                # Mandamos mensaje de confirmado
                flash('¡Registrado!')

                print(email)
                print(cipher)
                print(passwordConf)
                return redirect(url_for('Index'))
            else:
                flash("La contraseña no es igual")
                return Edit_user(id)


@app.route('/edit/<string:id>')
def Edit_user(id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (id))
    data = cur.fetchall()

    print(data[0])
    return render_template('restore-pass.html', user=data[0])


@app.route('/update/<id>', methods=['POST'])
def Update_user(id):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        passwordConf = request.form['passwordConf']

        if len(email) == 0 | len(password) == 0 | len(passwordConf) == 0:
            return Edit_user(id)
        else:
            cur = connection.cursor()

            # Verificar si la contraseña es de 8 digitos
            if len(password) != 8:
                flash("La contraseña debe de ser 8 digitos")
                return Edit_user(id)
            else:
                # Validar si las contraseñas son iguales
                if (password == passwordConf):
                    # Algoritmo de cifrado MD5
                    textUtf8 = password.encode("utf-8")
                    hash = hashlib.md5(textUtf8)
                    cipher = hash.hexdigest()

                    # Se agrega a la base de datos el email y el password cifrado
                    cur.execute("""
                        UPDATE users
                        SET email = %s,
                            pass = %s,
                            pass_ext = %s
                        WHERE id = %s
                    """, (email, cipher, passwordConf, id))
                    connection.commit()
                    flash("Usuario Actualizado")
                    return redirect(url_for('Index'))
                else:
                    flash("La contraseña  no es igual")
                    return Edit_user(id)


@app.route('/delete/<string:id>')
def Delete_user(id):
    cur = connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    connection.commit()
    flash('Se ha borrado correctamente')

    return redirect(url_for('Table'))

# Send Email
@app.route('/send', methods=["GET", "POST"])
def Send():
    if request.method == 'POST':
        email = request.form['email']
        if len(email) == 0:
            return redirect(url_for('Restore'))
        else:
            cur = connection.cursor()
            cur.execute('SELECT * FROM users WHERE email = %s',
                        (email,))
            data = cur.fetchone()
            cur.close()
            data
            # Create Message
            msg = Message('Practica - Restaurar Password',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[str(data[1])])

            msg.body = '¡Hola!\nAbre en el navegador o da click en este link para restaurar tu contraseña:\n\n' + \
                'http://cryp-log.herokuapp.com/edit/' + \
                str(data[0]) + '\n\n¡Un saludo!'
            mail.send(msg)

            flash('Se ha enviado el correo')
            return redirect(url_for('Index'))

# app and port
if __name__ == '__main__':
    mail.init_app(app)
    app.run(port=port_lh, debug=True)