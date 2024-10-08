# routes.py

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app import app, Session
from usuario import Usuario
from validaciones import Validaciones
from sqlalchemy.exc import IntegrityError
from OrdenServicio import OrdenServicio
from flask_login import current_user
from OrdenServicio import OrdenServicio
from Tecnico import Tecnico
from flask_login import login_required


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
        session.add(nueva_orden)
        session.commit()
        flash('Orden de servicio creada exitosamente.', 'success')
        session.close()
    return render_template('orden_servicio.html')

def ver_ordenes():
    if not current_user.is_authenticated:
        flash('User not authenticated', 'error')
        return redirect(url_for('inicio_sesion'))

    if not isinstance(current_user, Tecnico):
        flash('Access denied: User is not a technician', 'error')
        return redirect(url_for('menu'))

    session = Session()
    ordenes = session.query(OrdenServicio).all()
    session.close()
    return render_template('ver_ordenes.html', ordenes=ordenes)

@app.route('/crear_orden_servicio', methods=['POST'])
def crear_orden_servicio():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        correo_usuario = request.form['correo_usuario']
        
        # Aquí necesitas corregir el nombre del parámetro
        nueva_orden = OrdenServicio(correo=correo_usuario, descripcion=descripcion)
        
        session = Session()
        session.add(nueva_orden)
        session.commit()
        session.close()
        
        return redirect(url_for('menu'))
    

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/menu_tecnico')
def menu_tecnico():
    return render_template('menu_tecnico.html')

@app.route('/solicitud')
def solicitud():
    return render_template('solicitud.html')

@app.route('/equipo')
def equipo():
    return render_template('equipo.html')

@app.route('/ver_ordenes')
def ver_ordenes():
    session = Session()
    ordenes = session.query(OrdenServicio).all()
    session.close()
    return render_template('ver_ordenes.html', ordenes=ordenes)


def load_user(correo):
    session = Session()
    user = session.query(Usuario).filter_by(correo=correo).first()
    if not user:
        user = session.query(Tecnico).filter_by(correo=correo).first()
    session.close()
    return user