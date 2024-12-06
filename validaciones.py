from app import app, Session

class Validaciones:
    @staticmethod
    def validar_correo(correo):
        dominio_permitido = '@hotmail.com'
        return correo.endswith(dominio_permitido)

    @staticmethod
    def validar_contraseña(contraseña):
        return len(contraseña) <= 8 and contraseña.isdigit()

    @staticmethod
    def verificar_inicio_sesion(correo, contraseña, session):
        # Utiliza la sesión de la base de datos para consultar el usuario
        from usuario import Usuario
        usuario = session.query(Usuario).filter_by(correo=correo, contraseña=contraseña).first()
        return usuario is not None
    @staticmethod
    def verificar_inicio_sesion_tecnico(correo, contraseña, session: Session):
        from Tecnico import Tecnico
        tecnico = session.query(Tecnico).filter_by(correo=correo, contraseña=contraseña).first()
        return tecnico is not None

    @staticmethod
    def verificar_tipo_usuario(correo, contraseña, session: Session):
        from usuario import Usuario
        from Tecnico import Tecnico
        usuario = session.query(Usuario).filter_by(correo=correo, contraseña=contraseña).first()
        if usuario:
            return 'usuario'
        tecnico = session.query(Tecnico).filter_by(correo=correo, contraseña=contraseña).first()
        if tecnico:
            return 'tecnico'
        return None