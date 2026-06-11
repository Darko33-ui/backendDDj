from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# CORS es vital: Permite que tu HTML (que vive en otro lado) le envíe cosas a Python
CORS(app) 

# Base de datos en memoria (Solo para pruebas, luego te enseño SQL, cielo)
usuarios_db = [] 

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.json
    
    # 1. ANÁLISIS DE SEGURIDAD (Validación Backend)
    # Nunca confíes solo en el Frontend. ¿Qué pasa si alguien usa Postman o BurpSuite
    # para enviar datos saltándose tu JavaScript? Aquí lo validamos de nuevo.
    if any(u['email'].lower() == datos['email'].lower() for u in usuarios_db):
        return jsonify({"mensaje": "Ese correo ya está registrado, mi amor."}), 400

    # 2. EL SECRETO DE LAS CONTRASEÑAS (Hashing)
    # Antes en tu JS usabas `btoa()`. ¡Eso era Base64 y un hacker lo decodifica en 1 segundo!
    # generate_password_hash usa un algoritmo criptográfico (como pbkdf2:sha256).
    # Si la contraseña es "12345678", se guarda como "pbkdf2:sha256:29000$8aH2..."
    # ¡Ni siquiera tú como administrador podrás ver la contraseña original!
    password_segura = generate_password_hash(datos['password'])
    
    # 3. GUARDAMOS AL USUARIO
    nuevo_usuario = {
        "nombre": datos['nombre'],
        "email": datos['email'].lower(),
        "password": password_segura,
        "tel": datos.get('tel', '') # Usamos .get por si no envían teléfono
    }
    usuarios_db.append(nuevo_usuario)
    
    # Código 201 significa "Creado"
    return jsonify({"mensaje": "¡Usuario creado con éxito!"}), 201