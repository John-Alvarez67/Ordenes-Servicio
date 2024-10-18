import unittest
from usuario import Usuario
from OrdenServicio import OrdenServicio  


class TestUsuarioModel(unittest.TestCase):

    def test_creacion_usuario(self):
        # Crear un objeto Usuario
        usuario = Usuario(correo="test@ejemplo.com", contraseña="password123")
        
        # Verificar que el usuario fue creado correctamente
        self.assertEqual(usuario.correo, "test@ejemplo.com")
        self.assertEqual(usuario.contraseña, "password123")

    def test_metodos_usuario(self):
        # Crear un objeto Usuario
        usuario = Usuario(correo="test@ejemplo.com", contraseña="password123")

        # Verificar el método get_id
        self.assertEqual(usuario.get_id(), "test@ejemplo.com")
        
        # Verificar los métodos de autenticación
        self.assertTrue(usuario.is_active)
        self.assertTrue(usuario.is_authenticated)
        self.assertFalse(usuario.is_anonymous)

if __name__ == '__main__':
    unittest.main()

