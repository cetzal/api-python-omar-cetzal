from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Maneja la validación y transformación de datos de producto entre la API (JSON)
    """
    nombre = serializers.CharField(source='nombre')
    precio = serializers.DecimalField(source='precio', max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(source='stock')
    activo = serializers.BooleanField(source='activo', default=True)
    created = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Product
        # Los campos que se incluirán en la representación de la API.
        fields = [
            'id',
            'nombre',
            'precio',
            'stock',
            'activo',
            'created',
            'last_update',
        ]
        extra_kwargs = {
            # forzando campos requerido para el api
            'nombre': {'required': True},
            'precio': {'required': True},
            'stock': {'required': True},
        }

class ProductUpdateSerializer(ProductSerializer):
    """
    Serializer para actualización de productos (PUT/PATCH).
    Hereda de ProductSerializer pero hace opcional los campos.
    """
    class Meta(ProductSerializer.Meta):
        extra_kwargs = {
            **ProductSerializer.Meta.extra_kwargs,
            'nombre': {'required': False},
            'precio': {'required': False},
            'stock': {'required': False},
        }