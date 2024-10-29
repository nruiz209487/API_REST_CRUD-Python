#app/users/routes.py
import bcrypt
import json
from flask import Flask, request, Blueprint, jsonify
from flask_jwt_extended import create_access_token

# Crear un blueprint para los usuarios
usuariosBP = Blueprint('usuarios', __name__)

# Archivo donde se guardarán los usuarios
ficheroUsers = 'app/users/usuarios.json'

# Cargar los usuarios existentes del archivo
def cargaUsuarios():
    try:
        with open(ficheroUsers, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Guardar los usuarios en el archivo
def escribeFichero(fichero, data):
    with open(fichero, 'w') as file:
        json.dump(data, file, indent=4)

# Lista de usuarios cargada del archivo
users = cargaUsuarios()

@usuariosBP.post('/registro')
def registrar_usuario():
    user = request.get_json()
    
    # Verificamos que se haya proporcionado un nombre de usuario y una contraseña
    if 'username' not in user or 'password' not in user:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

    # Codificamos la contraseña y la hashamos
    password = user['password'].encode('utf-8')
    salt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password, salt).hex()

    # Machacamos el campo contraseña con el hash calculado
    user['password'] = hashPassword

    # Añadimos el usuario a la lista de usuarios
    users.append(user)

    # Reescribimos el fichero
    escribeFichero(ficheroUsers, users)

    return {"message": "Usuario registrado correctamente"}, 201

@usuariosBP.route('/login', methods=['POST'])
def login_usuario():
    users = cargaUsuarios()  # Cargar usuarios desde el archivo
    user_data = request.get_json()
    
    # Verificamos que se haya proporcionado un nombre de usuario y una contraseña
    if 'username' not in user_data or 'password' not in user_data:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

    username = user_data['username']
    password_input = user_data['password'].encode('utf-8')

    # Buscamos el usuario en la lista
    for user in users:
        if user['username'] == username:
            # El hash almacenado está en hexadecimal, lo convertimos a bytes
            password_stored = bytes.fromhex(user['password'])
            # Verificamos la contraseña
            if bcrypt.checkpw(password_input, password_stored):
                token = create_access_token(identity=username)
                return jsonify({"token": token}), 200
            else:
                return jsonify({"error": "Contraseña incorrecta"}), 401

    # Si no encontramos el usuario
    return jsonify({"error": "Usuario no encontrado"}), 404



