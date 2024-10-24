from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app import app, Session
from usuario import Usuario
from validaciones import Validaciones
from sqlalchemy.exc import IntegrityError
from OrdenServicio import OrdenServicio
from Tecnico import Tecnico
from flask_login import current_user

@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el registro de usuarios
@app.route('/registrar', methods=['POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        session = Session()
        # Validar correo electrónico
        if not Validaciones.validar_correo(correo):
            flash('El correo electrónico debe tener el dominio @hotmail.com', 'error')
            return redirect(url_for('index'))
        # Validar contraseña
        if not Validaciones.validar_contraseña(contraseña):
            flash('La contraseña debe ser un máximo de 8 dígitos numéricos', 'error')
            return redirect(url_for('index'))
        # Registrar usuario en la base de datos
        try:
            nuevo_usuario = Usuario(correo=correo, contraseña=contraseña)
            session.add(nuevo_usuario)
            session.commit()
            flash('Usuario registrado correctamente.', 'success')
        except IntegrityError:
            session.rollback()
            flash('El correo ya está registrado.', 'error')
        finally:
            session.close()
    return redirect(url_for('index'))

@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        session = Session()

        tecnico = session.query(Tecnico).filter_by(correo=correo, contraseña=contraseña).first()
        if tecnico:
            login_user(tecnico)
            session.close()
            return redirect(url_for('menu_tecnico'))

        usuario = session.query(Usuario).filter_by(correo=correo, contraseña=contraseña).first()
        if usuario:
            login_user(usuario)
            session.close()
            return redirect(url_for('menu'))

        flash('Credenciales inválidas. Inténtalo de nuevo.', 'error')
        session.close()
    return render_template('inicio_sesion.html')

@app.route('/orden_servicio', methods=['GET', 'POST'])
@login_required
def orden_servicio():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        nueva_orden = OrdenServicio(descripcion=descripcion, usuario_correo=current_user.correo)
        session = Session()
        try:
            session.add(nueva_orden)
            session.commit()
            flash('Orden de servicio creada exitosamente.', 'success')
        finally:
            session.close()
    return render_template('orden_servicio.html')

# Consolidación de ver_ordenes en una única ruta
@app.route('/ver_ordenes')
@login_required
def ver_ordenes():
    session = Session()
    try:
        if isinstance(current_user, Tecnico):
            ordenes = session.query(OrdenServicio).all()
        else:
            flash('Acceso denegado: Solo técnicos pueden ver las órdenes.', 'error')
            return redirect(url_for('menu'))
    finally:
        session.close()
    return render_template('ver_ordenes.html', ordenes=ordenes)

@app.route('/crear_orden_servicio', methods=['POST'])
def crear_orden_servicio():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        correo_usuario = request.form['correo_usuario']

        nueva_orden = OrdenServicio(correo=correo_usuario, descripcion=descripcion)

        session = Session()
        try:
            session.add(nueva_orden)
            session.commit()
        finally:
            session.close()

        return redirect(url_for('menu'))

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/menu_tecnico')
@login_required
def menu_tecnico():
    return render_template('menu_tecnico.html')

@app.route('/solicitud')
def solicitud():
    return render_template('solicitud.html')

@app.route('/equipo')
def equipo():
    return render_template('equipo.html')

# Función para cargar usuarios (simplificada)
def load_user(correo):
    session = Session()
    try:
        user = session.query(Usuario).filter_by(correo=correo).first()
        if not user:
            user = session.query(Tecnico).filter_by(correo=correo).first()
    finally:
        session.close()
    return user
