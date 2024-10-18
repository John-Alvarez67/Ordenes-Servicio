import unittest
from Tecnico import Tecnico
from OrdenServicio import OrdenServicio  

class TestTecnicoModel(unittest.TestCase):

    def test_creacion_tecnico(self):
        # Crear un objeto Tecnico
        tecnico = Tecnico(correo="tecnico@ejemplo.com", contraseña="password123")

        # Verificar que el tecnico fue creado correctamente
        self.assertEqual(tecnico.correo, "tecnico@ejemplo.com")
        self.assertEqual(tecnico.contraseña, "password123")

    def test_metodos_tecnico(self):
        # Crear un objeto Tecnico
        tecnico = Tecnico(correo="tecnico@ejemplo.com", contraseña="password123")

        # Verificar el método get_id
        self.assertEqual(tecnico.get_id(), "tecnico@ejemplo.com")
        
        # Verificar los métodos de autenticación
        self.assertTrue(tecnico.is_active)
        self.assertTrue(tecnico.is_authenticated)
        self.assertFalse(tecnico.is_anonymous)

if __name__ == '__main__':
    unittest.main()
