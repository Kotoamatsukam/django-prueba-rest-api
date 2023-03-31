from django.db import models
from datetime import date
# Create your models here.
class Articulo(models.Model):
    Id = models.AutoField(primary_key=True)
    Referencia = models.CharField(max_length=200)
    Nombre = models.CharField(max_length=100)
    Descripcion = models.CharField(max_length=300)
    PrecioSinImpuestos = models.FloatField()
    ImpuestoAplicable = models.FloatField()
    FechaCreacion = models.DateField(default=date.today())

    def __str__(self):
        return self.Nombre

class Pedido(models.Model):
    articulos = models.ManyToManyField(Articulo, through='ArticuloPedido') # Relacion muchos a muchos

    Id = models.AutoField(primary_key=True)
    PrecioTotalSinImpuestos = models.FloatField()
    PrecioTotalConImpuestos = models.FloatField()
    FechaCreacion = models.DateField(default=date.today())

    def __str__(self):
        return self.Id

class ArticuloPedido(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    referencia = models.CharField(max_length = 500, default = 'Sin referencia')

    def __str__(self):
        return "{}_{}".format(self.pedido.__str__(), self.articulo.__str__())




