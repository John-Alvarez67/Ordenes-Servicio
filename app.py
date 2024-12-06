from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import re

app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta'  # Necesaria para usar mensajes flash

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio_sesion'

# Simulando una base de datos de usuarios
usuarios = {
    'usuario@hotmail.com': {'id': 'usuario1', 'correo': 'usuario@hotmail.com', 'contraseña': '12345678'}
}

# Clase Usuario que implementa UserMixin
class Usuario(UserMixin):
    def __init__(self, id, correo, contraseña):
        self.id = id
        self.correo = correo
        self.contraseña = contraseña

    @property
    def email(self):
        return self.correo

    # Métodos requeridos por Flask-Login
    def is_authenticated(self):
        return True  # Usuario siempre autenticado cuando se logea correctamente

    def is_active(self):
        return True  # Siempre activo en este caso

    def is_anonymous(self):
        return False  # El usuario no es anónimo

# Cargar usuario por ID (esto es solo un ejemplo simple)
@login_manager.user_loader
def load_user(user_id):
    for usuario_data in usuarios.values():
        if usuario_data['id'] == user_id:
            return Usuario(usuario_data['id'], usuario_data['correo'], usuario_data['contraseña'])
    return None

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el registro de usuario
@app.route('/registro', methods=['POST'])
def registro():
    correo = request.form.get('correo')  # Obtén el correo ingresado
    contraseña = request.form.get('contraseña')  # Obtén la contraseña ingresada

    # Validación del correo
    if not correo.endswith('@hotmail.com'):
        flash('El correo debe ser del dominio @hotmail.com', 'error')
        return redirect(url_for('index'))

    # Validación de la contraseña
    if len(contraseña) > 8 or not contraseña.isdigit():
        flash('La contraseña debe ser solo de números y no mayor a 8 caracteres', 'error')
        return redirect(url_for('index'))

    # Simula el registro exitoso
    flash('Registro exitoso', 'success')
    return redirect(url_for('index'))

# Ruta para el inicio de sesión
@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        # Validar que el correo y contraseña existan
        if correo in usuarios and usuarios[correo]['contraseña'] == contraseña:
            user = Usuario(usuarios[correo]['id'], usuarios[correo]['correo'], usuarios[correo]['contraseña'])
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('menu'))  # Redirige al menú
        else:
            flash('Correo o contraseña incorrectos', 'error')
            return redirect(url_for('inicio_sesion'))

    return render_template('inicio_sesion.html')

# Ruta para el menú (solo accesible si el usuario está autenticado)
@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html', current_user=current_user)

# Ruta para cerrar sesión
@app.route('/cerrar_sesion')
@login_required
def cerrar_sesion():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('inicio_sesion'))

@app.route('/orden_servicio')
def orden_servicio():
    return render_template('orden_servicio.html')
@app.route('/solicitud', methods=['GET', 'POST'])
def solicitud():
    return render_template('solicitud.html')

if __name__ == '__main__':
    app.run(debug=True)
