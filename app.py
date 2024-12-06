from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from usuario import Base, Usuario
import os

# Configuración de Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración para archivos estáticos
app.static_folder = 'static'
app.static_url_path = '/static'

# Configuración de Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio_sesion'

# Cadena de conexión a PostgreSQL desde variables de entorno
connection_string = os.getenv('DATABASE_URL')  # Configura correctamente DATABASE_URL en Render

# Motor y sesión de base de datos
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))  # Usar scoped_session para manejo más seguro

# Cargar usuario para sesión
@login_manager.user_loader
def load_user(user_id):
    session = Session()
    try:
        return session.get(Usuario, user_id)  # Si estás usando SQLAlchemy 1.4+
    finally:
        session.close()

# Registrar Blueprints
from routes import app_routes
app.register_blueprint(app_routes)

# Asegurarse de remover la sesión al final del ciclo de vida de la app
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

# Ejecutar aplicación
if __name__ == '__main__':
    app.run(debug=True)
