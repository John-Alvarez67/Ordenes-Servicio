
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from usuario import Base
from flask_login import LoginManager
from usuario import Usuario
from flask import Flask, render_template, url_for, flash, redirect


app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Configuración para archivos estáticos
app.static_folder = 'static'
app.static_url_path = '/static'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inicio_sesion'

# Cadena de conexión a PostgreSQL
connection_string = 'postgresql://juan:12345678@db:5432/web'
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    user = session.query(Usuario).get(user_id)
    session.close()
    return user


if __name__ == '__main__':
    from routes import *
    app.run( debug=True)
