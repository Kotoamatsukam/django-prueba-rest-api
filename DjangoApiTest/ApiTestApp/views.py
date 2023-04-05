from ApiTestApp.models import Articulo, Pedido, PedidoArticulo
from ApiTestApp.serializers import ArticuloSerializer, PedidoSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from collections import namedtuple
from django.db import connection
@api_view(['GET','POST', 'PUT', 'DELETE'])
def articuloApi(request, pkArticulo = 0):
    if request.method == 'GET': # Para obtener todos los articulos
        if pkArticulo == 0:
            articulos = Articulo.objects.all()

        else:
            articulos = Articulo.objects.filter(Id = pkArticulo)
        articulos_serializer = ArticuloSerializer(articulos, many = True)
        return Response(articulos_serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':
        request.POST._mutable = True
        articulos_serializer = ArticuloSerializer(data = request.data)
        if articulos_serializer.is_valid():# si el modelo enviado es el correcto, guardamos en la base de datoss
            articulos_serializer.save()
            return Response("Articulo agregado correctamente", status=status.HTTP_200_OK)
        return Response("Error al agregar articulo", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        articulo = Articulo.objects.get(Id = request.data['Id'])
        request.POST._mutable = True
        articulo_serializer = ArticuloSerializer(articulo, data = request.data)
        if articulo_serializer.is_valid():
            articulo_serializer.save()
            return Response("Articulo actualizado correctamente", status=status.HTTP_200_OK)
        return Response("Error al actualizar el pedido", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        articulo = Articulo.objects.filter(Id = pkArticulo)
        articulo.delete()
        return  Response("Articulo eliminado con exito")

@api_view(['GET','POST', 'PUT'])
def pedidoApi(request, pkPedido = 0):

    if request.method == 'GET':
        c = connection.cursor()
        if pkPedido == 0:
            pedidos = Pedido.objects.all()
        else:
            pedidos = Pedido.objects.filter(Id = pkPedido)
        pedidos_serializer = PedidoSerializer(pedidos, many = True)
        for dict in pedidos_serializer.data:
            pedido_id = dict['Id']
            c = connection.cursor()
            c.execute('SELECT articulo_id FROM apitestdb.apitestapp_pedidoarticulo WHERE pedido_id = %s', pedido_id)
            nombres_articulos = []
            for row in c:
                art_obj = Articulo.objects.get(Id=row[0])
                if PedidoArticulo.objects.filter(articulo = art_obj, pedido = pedido_id).exists():
                    pedido_articulo = PedidoArticulo.objects.get(articulo=art_obj.Id, pedido = pedido_id)
                    tuple = (f'Nombre: {art_obj.Referencia}', f'Cantidad: {pedido_articulo.cantidad}')
                    nombres_articulos.append(tuple)

            dict['articulos'] = nombres_articulos# Agregamos este componente en el json de salida

        return Response(pedidos_serializer.data, status = status.HTTP_200_OK)

    elif request.method == 'POST':
        request.POST._mutable = True
        pedido_serializer = PedidoSerializer(data=request.data)
        if pedido_serializer.is_valid():  # si el modelo enviado es el correcto, guardamos en la base de datos
            pedido_serializer.save()
            return Response("El pedido se agrego correctamente",status = status.HTTP_200_OK)
        else:
            print(pedido_serializer.errors)
        return Response(pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        pedido = Pedido.objects.filter(Id = pkPedido).first() # usamos first para obtener solo 1 instancia
        request.POST._mutable = True
        pedido_serializer = PedidoSerializer(pedido, data=request.data)
        if pedido_serializer.is_valid():
            pedido_serializer.save()
            return Response("Articulo actualizado correctamente", status=status.HTTP_200_OK)
        return Response("Error al actualizar el pedido", status=status.HTTP_400_BAD_REQUEST)


