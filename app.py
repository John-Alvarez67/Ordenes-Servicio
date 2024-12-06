from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from usuario import Base, Usuario
import os
from routes import routes  # Importa el Blueprint

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración de Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio_sesion'

# Cadena de conexión a PostgreSQL desde variables de entorno
connection_string = os.getenv('DATABASE_URL')

# Motor y sesión de base de datos
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

# Cargar usuario para sesión
@login_manager.user_loader
def load_user(user_id):
    session = Session()
    try:
        return session.get(Usuario, user_id)
    finally:
        session.close()

# Registrar el Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

