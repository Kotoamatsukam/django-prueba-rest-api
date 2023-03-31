from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # para que otros dominios puedan acceder a los metodos
from rest_framework.parsers import JSONParser# Para parsear la data que viene en modelos
from django.http.response import JsonResponse

from ApiTestApp.models import Articulo, Pedido, ArticuloPedido
from ApiTestApp.serializers import ArticuloSerializer, PedidoSerializer


# Create your views here.
@csrf_exempt
def articuloApi(request, id = 0):
    if request.method == 'GET':
        articulos = Articulo.objects.all()
        articulos_serializer = ArticuloSerializer(articulos, many = True)
        return JsonResponse(articulos_serializer.data, safe = False)
    elif request.method == 'POST':
        articulo_data = JSONParser().parse(request)
        articulos_serializer = ArticuloSerializer(data = articulo_data)
        if articulos_serializer.is_valid():# si el modelo enviado es el correcto, guardamos en la base de datoss
            articulos_serializer.save()
            return JsonResponse("Articulo agregado correctamente", safe = False)
        return JsonResponse("Error al agregar el articulo", safe = False)
    elif request.method == 'PUT':
        articulo_data = JSONParser().parse(request)
        articulo = Articulo.objects.get(Id = articulo_data['Id'])# capturamos el registro actual por el id
        articulo_serializer = ArticuloSerializer(articulo, data = articulo_data)
        if articulo_serializer.is_valid():
            articulo_serializer.save()
            return JsonResponse("Articulo actualizado correctamente", safe = False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        articulo = Articulo.objects.get(Id = id)
        articulo.delete()
        return JsonResponse("Articulo eliminado correctamente", safe = False)

@csrf_exempt
def pedidoApi(request, id = 0):
    if request.method == 'GET':
        pedidos = Pedido.objects.all()
        pedidos_serializer = PedidoSerializer(pedidos, many = True)
        return JsonResponse(pedidos_serializer.data, safe = False)

    elif request.method == 'POST':
        pedido_data = JSONParser().parse(request)
        pedido_serializer = PedidoSerializer(data = pedido_data)
        if pedido_serializer.is_valid():# si el modelo enviado es el correcto, guardamos en la base de datoss
            pedido_serializer.save()
            return JsonResponse("Pedido agregado correctamente", safe = False)
        return JsonResponse(pedido_serializer.data())
    elif request.method == 'PUT':
        pedido_data = JSONParser().parse(request)
        pedido = Pedido.objects.get(Id = pedido_data['Id'])# capturamos el registro actual por el id
        pedido_serializer = PedidoSerializer(pedido, data = pedido_data)
        if pedido_serializer.is_valid():
            pedido_serializer.save()
            return JsonResponse("Pedido actualizado correctamente", safe = False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        pedido = Pedido.objects.get(Id = id)
        pedido.delete()
        return JsonResponse("Pedido eliminado correctamente", safe = False)