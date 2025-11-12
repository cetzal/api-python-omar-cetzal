from django.shortcuts import get_object_or_404
from .models import Product

class ProductRepository:
    """
    La clase ProductRepository es responsable de todas las operaciones de la base de datos relacionadas con el modelo de Producto.
    """

    def get_all_products(self, filters=None):
        queryset = Product.objects.all()
        
        if filters:
            if 'nombre' in filters:
                queryset = queryset.filter(nombre__icontains=filters['nombre'])

            if 'activo' in filters:
                is_active_val = str(filters.get('activo', '')).lower() in ['true', '1', 'yes']
                queryset = queryset.filter(activo=is_active_val)

            if 'precio_min' in filters:
                try:
                    precio_min_val = float(filters['precio_min'])
                    queryset = queryset.filter(precio__gte=precio_min_val)
                except (ValueError, TypeError):
                    pass

            if 'precio_max' in filters:
                try:
                    precio_max_val = float(filters['precio_max'])
                    queryset = queryset.filter(precio__lte=precio_max_val)
                except (ValueError, TypeError):
                    pass

            if 'stock' in filters:
                try:
                    stock_val = int(filters['stock'])
                    queryset = queryset.filter(stock=stock_val)
                except (ValueError, TypeError):
                    pass

        return queryset.order_by('id')

    def create_product(self, validated_data):
        return Product.objects.create(**validated_data)

    def get_product_by_id(self, product_id):
        return get_object_or_404(Product, id=product_id)

    def update_product(self, product, validated_data):
        product.nombre = validated_data.get('nombre', product.nombre)
        product.precio = validated_data.get('precio', product.precio)
        product.stock = validated_data.get('stock', product.stock)
        product.activo = validated_data.get('activo', product.activo)

        product.save()
        return product

    def delete_product(self, product):
        product.delete()