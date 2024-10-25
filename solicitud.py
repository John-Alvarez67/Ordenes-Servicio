# solicitud.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from usuario import Base  # Importa Base de tu configuración actual

class SolicitudReparacion(Base):
    __tablename__ = 'solicitudes_reparacion'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=True)
    nombre_equipo = Column(String(100), nullable=False)
    modelo_equipo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_solicitud = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<SolicitudReparacion(nombre='{self.nombre}', correo='{self.correo}')>"
