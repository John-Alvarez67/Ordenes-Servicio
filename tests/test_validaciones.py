import unittest
from unittest.mock import MagicMock
from validaciones import Validaciones  # Ajusta la importación según la ubicación de validaciones.py

class TestValidaciones(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()  # Mock para la sesión de base de datos

    def test_validar_correo(self):
        self.assertTrue(Validaciones.validar_correo("usuario@hotmail.com"))
        self.assertFalse(Validaciones.validar_correo("usuario@gmail.com"))

    def test_validar_contraseña(self):
        self.assertFalse(Validaciones.validar_contraseña("12345678"))  # Demasiado larga
        self.assertTrue(Validaciones.validar_contraseña("1234567"))    # Aceptada (7 dígitos)
        self.assertFalse(Validaciones.validar_contraseña("abcd1234"))  # No es solo dígitos

    def test_verificar_inicio_sesion(self):
        # Simula que no se encuentra el usuario
        self.session.query().filter_by().first.return_value = None
        self.assertFalse(Validaciones.verificar_inicio_sesion("usuario@hotmail.com", "password123", self.session))

        # Simula que se encuentra un usuario
        self.session.query().filter_by().first.return_value = MagicMock()
        self.assertTrue(Validaciones.verificar_inicio_sesion("usuario@hotmail.com", "password123", self.session))

    def test_verificar_tipo_usuario(self):
        # Simula que no se encuentra el usuario ni el técnico
        self.session.query().filter_by().first.return_value = None
        self.assertIsNone(Validaciones.verificar_tipo_usuario("usuario@hotmail.com", "password123", self.session))

        # Simula que se encuentra un usuario
        self.session.query().filter_by().first.return_value = MagicMock()
        self.assertEqual(Validaciones.verificar_tipo_usuario("usuario@hotmail.com", "password123", self.session), 'usuario')

if __name__ == '__main__':
    unittest.main()
