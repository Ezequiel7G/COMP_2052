from flask import Flask, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, identity_loaded, AnonymousIdentity

app = Flask(__name__)
app.secret_key = 'supersecretkey'


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


principals = Principal(app)


usuarios = {
    'adminuser': {'password': 'adminpass', 'role': 'admin'},
    'normaluser': {'password': 'userpass', 'role': 'user'}
}

# Permisos
permiso_admin = Permission(RoleNeed('admin'))
permiso_user = Permission(RoleNeed('user'))


@login_manager.user_loader
def cargar_usuario(user_id):
    if user_id in usuarios:
        user = {'id': user_id, 'role': usuarios[user_id]['role']}
        return user
    return None


def crear_usuario(user_id):
    user = {'id': user_id, 'role': usuarios[user_id]['role']}
    return user


@identity_loaded.connect_via(app)
def cargar_roles(sender, identity):
    user_id = session.get('user_id')
    if user_id and user_id in usuarios:
        identity.provides.add(RoleNeed(usuarios[user_id]['role']))


@app.route('/')
def inicio():
    return 'Bienvenido al inicio público de la app!'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = usuarios.get(username)

    if user and user['password'] == password:
        session['user_id'] = username
        identity_changed.send(app, identity=Identity(username))
        return jsonify({'mensaje': f'Login exitoso como {user["role"]}'})
    else:
        return jsonify({'mensaje': 'Usuario o password incorrectos'}), 401


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    identity_changed.send(app, identity=AnonymousIdentity())
    return jsonify({'mensaje': 'Logout exitoso'})


@app.route('/admin')
@login_required
@permiso_admin.require(http_exception=403)
def admin():
    return jsonify({'mensaje': f'Hola Admin {session.get("user_id")}!'})


@app.route('/profile')
@login_required
@permiso_user.require(http_exception=403)
def perfil():
    return jsonify({'mensaje': f'Hola Usuario {session.get("user_id")}!'})


# Correr el servidor
if __name__ == '__main__':
    app.run(debug=True)
