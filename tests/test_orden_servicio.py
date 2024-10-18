import unittest
from OrdenServicio import OrdenServicio  # Asegúrate de que la ruta sea correcta

class TestOrdenServicio(unittest.TestCase):

    def test_crear_orden_servicio(self):
        # Crea una nueva orden de servicio
        orden = OrdenServicio(correo='test_user@hotmail.com', descripcion='Descripción de prueba')
        self.assertIsNotNone(orden)  # Verifica que la instancia no sea None

    def test_repr(self):
        orden = OrdenServicio(correo='test_user@hotmail.com', descripcion='Descripción de prueba')
        self.assertEqual(repr(orden), "<OrdenServicio(descripcion='Descripción de prueba')>")  # Verifica la representación

if __name__ == '__main__':
    unittest.main()
