from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, current_user, logout_user
from usuario import Usuario
from validaciones import Validaciones
from sqlalchemy.exc import IntegrityError
from OrdenServicio import OrdenServicio
from Tecnico import Tecnico
from solicitud import SolicitudReparacion
from app import Session

# Crear Blueprint
app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    return render_template('index.html')

@app_routes.route('/registrar', methods=['POST'])
def registro():
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    session = Session()
    try:
        if not Validaciones.validar_correo(correo):
            flash('El correo debe ser @hotmail.com', 'error')
            return redirect(url_for('app_routes.index'))
        if not Validaciones.validar_contraseña(contraseña):
            flash('La contraseña debe ser un máximo de 8 dígitos.', 'error')
            return redirect(url_for('app_routes.index'))
        
        nuevo_usuario = Usuario(correo=correo, contraseña=contraseña)
        session.add(nuevo_usuario)
        session.commit()
        flash('Usuario registrado correctamente.', 'success')
    except IntegrityError:
        session.rollback()
        flash('El correo ya está registrado.', 'error')
    finally:
        session.close()
    return redirect(url_for('app_routes.index'))

@app_routes.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        session = Session()
        try:
            usuario = session.query(Usuario).filter_by(correo=correo, contraseña=contraseña).first()
            if usuario:
                login_user(usuario)
                return redirect(url_for('app_routes.menu'))
            flash('Credenciales inválidas.', 'error')
        finally:
            session.close()
    return render_template('inicio_sesion.html')

@app_routes.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app_routes.route('/menu_tecnico')
@login_required
def menu_tecnico():
    return render_template('menu_tecnico.html')

@app_routes.route('/orden_servicio', methods=['GET', 'POST'])
@login_required
def orden_servicio():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        session = Session()
        try:
            nueva_orden = OrdenServicio(descripcion=descripcion, usuario_correo=current_user.correo)
            session.add(nueva_orden)
            session.commit()
            flash('Orden creada exitosamente.', 'success')
        finally:
            session.close()
    return render_template('orden_servicio.html')

@app_routes.route('/solicitud', methods=['GET', 'POST'])
def solicitud():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        nueva_solicitud = SolicitudReparacion(nombre=nombre, descripcion=descripcion)
        session = Session()
        try:
            session.add(nueva_solicitud)
            session.commit()
            flash('Solicitud creada.', 'success')
        finally:
            session.close()
    return render_template('solicitud.html')
