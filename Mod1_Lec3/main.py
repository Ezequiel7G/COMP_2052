from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        "name": "John Doe",
        "email": "johnDoe@outlook.com",

    },
    {
        "name": "Bobby Fisher",
        "email": "bobbyfisher@outlook.com"
    }
]


@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "app": "Data management",
        "ver": "1.0",
        "developer": "Ezequiel Gerena Rivas",
        "status": "Active"
    }), 200


@app.route('/create_user', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibio ningun dato."}), 400

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Faltan datos: nombre y correo son obligatorios."}), 400

    new_user = {"name": name, "email": email}
    users.append(new_user)

    return jsonify({"mensaje": "Usuario creado exitosamente.", "user": new_user}), 201


@app.route('/users', methods=['GET'])
def listar_usuarios():
    return jsonify(users), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada."}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor."}), 500


if __name__ == '__main__':
    app.run(debug=True)
