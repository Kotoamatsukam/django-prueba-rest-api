from django.urls import re_path as url
from ApiTestApp import views

urlpatterns = [
    url(r'^articulo$', views.articuloApi),
    url(r'^articulo/([0-9]+)$', views.articuloApi),# El metodo delete necesita de un id
    url(r'^pedido$', views.pedidoApi),
    url(r'^pedido/([0-9]+)$', views.pedidoApi)
]