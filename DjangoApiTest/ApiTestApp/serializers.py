from rest_framework import serializers
from ApiTestApp.models import Articulo, Pedido, ArticuloPedido
# from DjangoApiTest.ApiTestApp
class ArticuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articulo
        fields = ('Id', 'Referencia', 'Nombre',
                  'Descripcion', 'PrecioSinImpuestos', 'ImpuestoAplicable',
                  'FechaCreacion')
class PedidoSerializer(serializers.ModelSerializer):
    articulos = ArticuloSerializer(many = True, read_only=True)
    # Obtenemos las listas de las primary keys
    articulos_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Articulo.objects.all())
    class Meta:
        model = Pedido
        fields = ('articulos', 'articulos_ids', 'Id', 'PrecioTotalSinImpuestos', 'PrecioTotalConImpuestos',
                  'FechaCreacion')

    def create(self, validated_data):
        # data = validated_data['data']


        # articulos = validated_data.pop('articulos_ids', None)
        # validated_data["articulos_ids"] = self.context["articulos_ids"].Id
        pedido = Pedido.objects.create(PrecioTotalSinImpuestos = validated_data['PrecioTotalSinImpuestos'],
                                       PrecioTotalConImpuestos = validated_data['PrecioTotalConImpuestos'])
        print(validated_data)
        for id in validated_data['articulos_ids']:
            articulo_obj = Articulo.objects.get("Id" == id)
            pedido.articulos.add(articulo_obj)
        return pedido


# https://stackoverflow.com/questions/67344416/post-request-manytomany-field-drf-with-postman
#     def create(self, validated_data):
#         articulos = validated_data.pop("articulos_ids", None)
#         pedido =

# class ArticuloPedidoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArticuloPedido
#         fields = ('articulo', 'pedido', 'cantidad')