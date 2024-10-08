
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    correo = Column(String, primary_key=True)
    contraseña = Column(String, nullable=False)
    ordenes_servicio = relationship('OrdenServicio', back_populates='usuario')

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