# librerias / libraries
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL, MySQLdb
# from flask_login import LoginManager
import bcrypt

# import mysql.connector
# from mysql.connector import Error

# inicializaciones / initializations
app = Flask("__name__")

# login = LoginManager(app)
# conexion con la base de datos / database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'backend_360'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# encriptamiento

# settings


# rutas / routes
@app.route('/')
def Index():
    if 'n_usuario' in session:
        return render_template('solicitudes.html')
    else:
        return render_template('login.html')


'''@app.route('/', methods=['POST'])
def autenticacion():
    usuario = request.form['correo']
    contrasena = request.form['contrasena']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario WHERE correo = '" + usuario + "'and password'" + contrasena + "'")
    data = cur.fetchone()
    if data is None:
        return "Correo o Contraseña erroneos"
    else:
        return render_template('solicitudes.html')
'''


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        n_usuario = request.form['n_usuario']
        contrasena = request.form['contrasena'].encode('utf-8')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM usuario WHERE n_usuario = %s", (n_usuario,))
        user = cur.fetchone()
        cur.close()

        if len(user) > 0:
            if bcrypt.hashpw(contrasena, user['contrasena'].encode('utf-8')) == user['contrasena'].encode('utf-8'):
                session['n_usuario'] = user['n_usuario']
                session['correo'] = user['correo']
                return render_template('solicitudes.html')
        else:
            return "Error, usuario o contraseña no coinciden"
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")


@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        n_usuario = request.form['n_usuario']
        correo = request.form['correo']
        contrasena = request.form['contrasena'].encode('utf-8')
        hash_contrasena = bcrypt.hashpw(contrasena, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (n_usuario, correo, contrasena) VALUES (%s, %s, %s)",
                    (n_usuario, correo, hash_contrasena))
        mysql.connection.commit()
        session['n_usuario'] = n_usuario
        session['correo'] = correo
        return render_template('login.html')


@app.route('/solicitudes')
def solicitudes():
    return render_template('solicitudes.html')


@app.route('/cargar', methods=['POST'])
def cargar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        #asunto = request.form['asunto']
        detalle = request.form['detalle']
        id_usuario = 19
        id_solicitante = 2
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO solicitantes (nombre, apellido, correo, telefono, id_usuario) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellido, correo, telefono, id_usuario))
        cur.execute("INSERT INTO solicitud (detalle, id_solicitante) VALUES (%a, %a)",
                    (detalle, id_solicitante))
        # cur.excute("INSERT INTO asunto (asunto) VALUES (%s)", (asunto,))
        mysql.connection.commit()
        return render_template('solicitudes.html')


# iniciando la aplicacion  / starting the app
if __name__ == "__main__":
    app.secret_key = "mysecretkey"
    app.run(port=3000, debug=True)
