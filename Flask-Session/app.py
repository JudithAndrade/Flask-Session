from flask import Flask, request, session, jsonify, redirect, url_for, render_template
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'  # Clave secreta para las sesiones
bcrypt = Bcrypt(app)

# Simular una base de datos de usuarios (diccionario en memoria)
users_db = {}

# Decorador para verificar si el usuario está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({"error": "No estás autenticado. Inicia sesión."}), 401
        return f(*args, **kwargs)
    return decorated_function

# Ruta principal (cargar la página de login/registro)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para registrar usuarios (POST)
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Nombre de usuario y contraseña son obligatorios."}), 400

    if username in users_db:
        return jsonify({"error": "El usuario ya está registrado."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users_db[username] = hashed_password

    return jsonify({"message": "Usuario registrado exitosamente."}), 201

# Ruta para iniciar sesión (POST)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username not in users_db or not bcrypt.check_password_hash(users_db[username], password):
        return jsonify({"error": "Credenciales incorrectas."}), 401

    session['username'] = username
    return jsonify({"message": "Inicio de sesión exitoso."}), 200

# Ruta para cerrar sesión (POST)
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('username', None)  # Eliminar la sesión del usuario
    return jsonify({"message": "Cierre de sesión exitoso."}), 200

# Ruta protegida (GET)
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return jsonify({"message": f"Bienvenido {session['username']} al dashboard."}), 200

if __name__ == '__main__':
    app.run(debug=True)

