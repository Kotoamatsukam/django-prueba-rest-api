from django.test import TestCase
from rest_framework.serializers import ValidationError
from .models import Articulo, Pedido
from .serializers import PedidoSerializer, ArticuloSerializer

# Create your tests here.

class PedidoSerializerTestCase(TestCase):
    # Creamos articulos para este caso
    def test_create_pedido_con_articulos_sin_repetir(self):
        articulo1 = Articulo.objects.create(Referencia = "Mermelada Laive", Nombre = "Mermelada azucarada",
                                            Descripcion = "300gr de mermelada laive", PrecioSinImpuestos = 13.2,
                                            ImpuestoAplicable = 18.2)
        articulo2 = Articulo.objects.create(Referencia="Cereal Zucaritas", Nombre="Cereal Zucaritas",
                                            Descripcion="500gr de cereal para desayuno", PrecioSinImpuestos=24.5,
                                            ImpuestoAplicable=18.2)
        articulo3 = Articulo.objects.create(Referencia="Aceite Vegetal", Nombre="Aceite Cocinero",
                                            Descripcion="400ml de aceite cocinero", PrecioSinImpuestos=30.8,
                                            ImpuestoAplicable=18.2)
        articulo4 = Articulo.objects.create(Referencia="Yogurt Gloria", Nombre="Yogurt Gloria",
                                            Descripcion="600gr de yogurt gloria", PrecioSinImpuestos=50.4,
                                            ImpuestoAplicable=19.2)

        # Creamos el diccionario para mandar al serializer
        validated_data = {
            'articulos': [articulo1.Id, articulo2.Id, articulo3.Id, articulo4.Id]
        }

        # Creamos el serializer para probar la instancia con la data creada
        serializer = PedidoSerializer(data = validated_data)

        self.assertTrue(serializer.is_valid())

        pedido = serializer.create(serializer.validated_data)

        self.assertAlmostEqual(pedido.PrecioTotalSinImpuestos, 118.9)
        self.assertAlmostEqual(pedido.PrecioTotalConImpuestos, 141.04)

    def test_create_pedido_con_articulos_repetidos(self):
        articulo1 = Articulo.objects.create(Referencia="Mermelada Laive", Nombre="Mermelada azucarada",
                                            Descripcion="300gr de mermelada laive", PrecioSinImpuestos=13.2,
                                            ImpuestoAplicable=18.2)
        articulo2 = Articulo.objects.create(Referencia="Cereal Zucaritas", Nombre="Cereal Zucaritas",
                                            Descripcion="500gr de cereal para desayuno", PrecioSinImpuestos=24.5,
                                            ImpuestoAplicable=18.2)
        articulo3 = Articulo.objects.create(Referencia="Aceite Vegetal", Nombre="Aceite Cocinero",
                                            Descripcion="400ml de aceite cocinero", PrecioSinImpuestos=30.8,
                                            ImpuestoAplicable=18.2)

        # Creamos el diccionario para mandar al serializer
        validated_data = {
            'articulos': [articulo1.Id, articulo2.Id, articulo1.Id, articulo1.Id, articulo3.Id]
        }

        # Creamos el serializer para probar la instancia con la data creada
        serializer = PedidoSerializer(data=validated_data)

        self.assertTrue(serializer.is_valid())

        pedido = serializer.create(serializer.validated_data)

        self.assertAlmostEqual(pedido.PrecioTotalSinImpuestos, 94.9)
        self.assertAlmostEqual(pedido.PrecioTotalConImpuestos, 112.1718)