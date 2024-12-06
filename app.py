from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta'  # Necesaria para usar mensajes flash

login_manager = LoginManager()
login_manager.init_app(app)

# Modelo de usuario (para la demostración)
class Usuario:
    def __init__(self, id, correo, contraseña):
        self.id = id
        self.correo = correo
        self.contraseña = contraseña

    def get_id(self):
        return self.id

    @property
    def email(self):
        return self.correo

# Simulamos un usuario almacenado
usuarios = {'usuario@hotmail.com': Usuario(1, 'usuario@hotmail.com', '12345678')}

# Cargar usuario por ID
@login_manager.user_loader
def load_user(user_id):
    return usuarios.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')

    if not correo.endswith('@hotmail.com'):
        flash('El correo debe ser del dominio @hotmail.com', 'error')
        return redirect(url_for('index'))

    if len(contraseña) > 8 or not contraseña.isdigit():
        flash('La contraseña debe ser solo números y no más de 8 caracteres', 'error')
        return redirect(url_for('index'))

    flash('Registro exitoso', 'success')
    return redirect(url_for('index'))

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        if correo in usuarios and usuarios[correo].contraseña == contraseña:
            login_user(usuarios[correo])
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('menu'))
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('inicio_sesion.html')

# Ruta para el menú principal
@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
