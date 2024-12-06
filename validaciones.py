# validaciones.py
def validar_correo(correo):
    # Lógica de validación para el correo
    if '@hotmail.com' not in correo:
        return False
    return True

def validar_contraseña(contraseña):
    # Lógica de validación para la contraseña
    if len(contraseña) > 8 or not contraseña.isdigit():
        return False
    return True

# Aquí añadimos una función que obtiene el 'app' y 'Session' solo cuando los necesitemos
def obtener_app_y_session():
    from app import app, Session  # Importar aquí evita el ciclo circular
    return app, Session
