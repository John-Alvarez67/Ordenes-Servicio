from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from usuario import Base
from sqlalchemy import Column, String, ForeignKey


class OrdenServicio(Base):
    __tablename__ = 'ordenes_servicio'
    id = Column(Integer, primary_key=True)
    correo = Column(String, ForeignKey('usuarios.correo'))
    descripcion = Column(String)
    usuario = relationship('Usuario', back_populates='ordenes_servicio')
    
    def __repr__(self):
        return f"<OrdenServicio(descripcion='{self.descripcion}')>"
