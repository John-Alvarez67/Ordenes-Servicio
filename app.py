from flask import Flask, render_template, request, redirect, url_for, flash

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
    if len(contraseña) > 8:
        flash('La contraseña no debe tener más de 8 caracteres', 'error')
        return redirect(url_for('index'))

    # Simula el registro exitoso
    flash('Registro exitoso', 'success')
    return redirect(url_for('index'))

# Ruta para el inicio de sesión
@app.route('/inicio_sesion')
def inicio_sesion():
    return "Página de inicio de sesión (en desarrollo)"  # Puedes personalizar esta página

if __name__ == '__main__':
    app.run(debug=True)
