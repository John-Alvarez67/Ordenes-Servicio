from sqlalchemy import Column, String , Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()

class Tecnico(Base):
    __tablename__ = 'tecnico'
    correo = Column(String, primary_key=True)
    contraseña = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


    def get_id(self):
        return self.correo

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
