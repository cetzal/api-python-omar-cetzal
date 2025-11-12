from django.db import models


class Product(models.Model):
    """
    Modelo que representa un producto en el sistema
    """
    nombre = models.CharField(max_length=255, verbose_name="Nombre del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del producto")
    stock = models.PositiveIntegerField(verbose_name="Cantidad en stock")
    activo = models.BooleanField(default=True, verbose_name="Producto activo")

    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['id']