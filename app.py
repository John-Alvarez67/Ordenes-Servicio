from flask import Flask, render_template, request, redirect, url_for, flash
import re  # Para la validación del correo y la contraseña

app = Flask(__name__)
app.secret_key = 'alguna_clave_secreta'  # Necesaria para usar mensajes flash

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
        flash('La contraseña debe ser solo números y no más de 8 caracteres', 'error')
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

        # Validación del correo (solo @hotmail.com)
        if not correo.endswith('@hotmail.com'):
            flash('El correo debe ser del dominio @hotmail.com', 'error')
            return redirect(url_for('inicio_sesion'))

        # Validación de la contraseña (solo números y máximo 8 caracteres)
        if len(contraseña) > 8 or not contraseña.isdigit():
            flash('La contraseña debe ser solo números y no más de 8 caracteres', 'error')
            return redirect(url_for('inicio_sesion'))

        # Simulación de credenciales válidas
        usuario_valido = correo == 'usuario@hotmail.com' and contraseña == '12345678'

        if usuario_valido:
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('menu'))  # Redirige al menú
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('inicio_sesion.html')

# Ruta para el menú principal
@app.route('/menu')
def menu():
    return render_template('menu.html')  # Crea esta plantilla para tu menú principal

if __name__ == '__main__':
    app.run(debug=True)
