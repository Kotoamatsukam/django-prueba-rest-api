from rest_framework import serializers
from ApiTestApp.models import Articulo, Pedido, PedidoArticulo
from datetime import datetime
# from DjangoApiTest.ApiTestApp

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
class ArticuloSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = '__all__'
class PedidoSerializer(DynamicFieldsModelSerializer,serializers.ModelSerializer):
    # articulos = ArticuloSerializer(many = True)
    articulos = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Articulo.objects.all())
    class Meta:
        model = Pedido
        fields = '__all__'
        extra_kwargs = {
            'articulos': {'required': True},
        }

    def create(self, validated_data):
        articulos = validated_data.get('articulos')
        precio_total_sin_impuestos = 0
        precio_total_con_impuestos = 0
        for obj_articulo in articulos:
            precio_total_sin_impuestos += obj_articulo.PrecioSinImpuestos
            precio_total_con_impuestos += obj_articulo.PrecioSinImpuestos*(1 + obj_articulo.ImpuestoAplicable/100)
        pedido = Pedido.objects.create(PrecioTotalSinImpuestos=precio_total_sin_impuestos, PrecioTotalConImpuestos=
        precio_total_con_impuestos, FechaCreacion=datetime.now())

        for obj_articulo in articulos:
            if PedidoArticulo.objects.filter(articulo = obj_articulo, pedido = pedido).exists():
                pedido_articulo = PedidoArticulo.objects.get(articulo = obj_articulo, pedido = pedido)
                pedido_articulo.cantidad = pedido_articulo.cantidad + 1
                pedido_articulo.save()
            else:
                # Si no existe el pedido, tenemos que crearlo, mediante ambas clases anteriormente mencionadas
                pedido_articulo = PedidoArticulo.objects.create(articulo = obj_articulo, pedido = pedido)
                pedido_articulo.save()
            pedido.articulos.add(obj_articulo)
        return pedido

