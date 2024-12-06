from flask import Flask, render_template, url_for, flash, redirect
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from usuario import Base, Usuario
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración para archivos estáticos
app.static_folder = 'static'
app.static_url_path = '/static'

# Configuración de Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio_sesion'

# Cadena de conexión a PostgreSQL desde variables de entorno (más seguro)
connection_string = os.getenv('DATABASE_URL', 'postgresql://juan:12345678@localhost:5432/web')

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

# Rutas importadas desde otro módulo
if __name__ == '__main__':
    from routes import *
    app.run(debug=True)

# Asegurarse de remover la sesión al final del ciclo de vida de la app
@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()
# Obtén la URL de la base de datos desde la variable de entorno
Database = os.getenv("Database")

# Configura el motor de SQLAlchemy
engine = create_engine(Database)

# (Si usas declarative_base o metadata)
Base.metadata.create_all(engine)