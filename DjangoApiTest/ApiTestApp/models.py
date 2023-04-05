from django.db import models
from datetime import datetime
# Create your models here.
class Articulo(models.Model):
    Id = models.AutoField(primary_key=True)
    Referencia = models.CharField(max_length=200)
    Nombre = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=300)
    PrecioSinImpuestos = models.FloatField()
    ImpuestoAplicable = models.FloatField()
    FechaCreacion = models.DateField(default=datetime.now())

class Pedido(models.Model):
    articulos = models.ManyToManyField(Articulo, through = 'PedidoArticulo') # Relacion muchos a muchos
    Id = models.AutoField(primary_key=True)
    PrecioTotalSinImpuestos = models.FloatField(blank= True)
    PrecioTotalConImpuestos = models.FloatField(blank= True)
    FechaCreacion = models.DateField(blank= True)


class PedidoArticulo(models.Model):
    Id = models.AutoField(primary_key=True)
    articulo = models.ForeignKey("Articulo", on_delete= models.CASCADE)
    pedido = models.ForeignKey("Pedido", on_delete = models.CASCADE)
    cantidad = models.IntegerField(default = 1)






