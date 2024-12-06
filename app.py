from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from validaciones import obtener_app_y_session
from usuario import Usuario
from sqlalchemy.exc import IntegrityError
from OrdenServicio import OrdenServicio
from Tecnico import Tecnico
from solicitud import SolicitudReparacion
import validaciones

# Obtener la instancia de app y Session desde validaciones.py para evitar import circular
app, Session = obtener_app_y_session()

# Ruta para el registro de usuarios
@app.route('/registrar', methods=['POST'])
def registro():
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    session = Session()

    # Validar correo electrónico
    if not validaciones.validar_correo(correo):
        flash('El correo electrónico debe tener el dominio @hotmail.com', 'error')
        return redirect(url_for('index'))

    # Validar contraseña
    if not validaciones.validar_contraseña(contraseña):
        flash('La contraseña debe ser un máximo de 8 dígitos numéricos', 'error')
        return redirect(url_for('index'))

    try:
        # Registrar usuario en la base de datos
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

# Ruta para iniciar sesión
@app.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        session = Session()

        # Buscar al usuario o técnico en la base de datos
        usuario = session.query(Usuario).filter_by(correo=correo, contraseña=contraseña).first()
        tecnico = session.query(Tecnico).filter_by(correo=correo, contraseña=contraseña).first()

        if usuario:
            login_user(usuario)
            return redirect(url_for('menu'))
        elif tecnico:
            login_user(tecnico)
            return redirect(url_for('menu_tecnico'))
        else:
            flash('Credenciales inválidas. Inténtalo de nuevo.', 'error')

        session.close()

    return render_template('inicio_sesion.html')

# Ruta para órdenes de servicio
@app.route('/orden_servicio', methods=['GET', 'POST'])
@login_required
def orden_servicio():
    session = Session()
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        nueva_orden = OrdenServicio(descripcion=descripcion, usuario_correo=current_user.correo)

        try:
            session.add(nueva_orden)
            session.commit()
            flash('Orden de servicio creada exitosamente.', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Error al crear la orden: {str(e)}', 'error')
        finally:
            session.close()

    # Listar órdenes de servicio para el usuario actual
    ordenes = session.query(OrdenServicio).filter_by(usuario_correo=current_user.correo).all()
    session.close()
    return render_template('orden_servicio.html', ordenes=ordenes)

# Ruta para el menú principal del usuario
@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

# Ruta para el menú del técnico
@app.route('/menu_tecnico')
@login_required
def menu_tecnico():
    session = Session()
    ordenes = session.query(OrdenServicio).all()
    session.close()
    return render_template('menu_tecnico.html', ordenes=ordenes)

# Ruta para solicitudes de reparación
@app.route('/solicitud', methods=['GET', 'POST'])
def solicitud():
    if request.method == 'POST':
        # Crear nueva solicitud
        nueva_solicitud = SolicitudReparacion(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            telefono=request.form['telefono'],
            direccion=request.form.get('direccion'),
            nombre_equipo=request.form['nombre_equipo'],
            modelo_equipo=request.form['modelo_equipo'],
            descripcion=request.form['descripcion']
        )

        session = Session()
        try:
            session.add(nueva_solicitud)
            session.commit()
            flash('Solicitud de reparación creada exitosamente.', 'success')
        except Exception as e:
            session.rollback()
            flash(f'Error al crear la solicitud: {str(e)}', 'error')
        finally:
            session.close()

    return render_template('solicitud.html')
