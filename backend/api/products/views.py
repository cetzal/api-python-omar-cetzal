from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer, ProductUpdateSerializer
from .services import ProductService


class ProductListCreateAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    @swagger_auto_schema(
        operation_summary="Listar productos",
        operation_description=(
            "Obtiene la lista de productos registrados en el sistema. "
            "Permite aplicar filtros opcionales como nombre, estado activo, "
            "rango de precios y stock."
        ),
        manual_parameters=[
            openapi.Parameter(
                'nombre',
                openapi.IN_QUERY,
                description="Filtra productos por nombre (búsqueda parcial, sin distinción de mayúsculas).",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'activo',
                openapi.IN_QUERY,
                description="Filtra por estado activo (true/false).",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'stock',
                openapi.IN_QUERY,
                description="Filtra productos por cantidad exacta de stock.",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                description="Lista de productos obtenida correctamente.",
                schema=ProductSerializer(many=True)
            ),
        },
    )
    
    def get(self, request):
        products = self.service.get_all_products(request.query_params)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Crear un nuevo producto",
        operation_description=(
            "Crea un nuevo producto en el sistema con los datos proporcionados. "
            "Valida los campos requeridos antes de almacenarlos."
        ),
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                description="Producto creado correctamente.",
                schema=ProductSerializer(),
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "El producto se ha creado correctamente",
                        "data": {
                            "id": 1,
                            "nombre": "Laptop Dell XPS 13",
                            "precio": "25999.00",
                            "stock": 15,
                            "activo": True,
                            "created": "2025-11-12T04:25:13Z",
                            "last_update": "2025-11-12T04:25:13Z",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Error de validación en los datos enviados."
            ),
        },
    )

    def post(self, request):
        """
        Crea un nuevo producto con los datos proporcionados en el cuerpo de la solicitud.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            created_product = self.service.create_product(serializer.validated_data)
            response_serializer = ProductSerializer(created_product)
            return Response(
                {
                    "status": "success",
                    "message": "El producto se ha creado correctamente",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyAPIView(APIView):
    """
    Métodos para interactuar con un producto en específico.
    Endpoint: /products/<int:product_id>/
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    @swagger_auto_schema(
        operation_summary="Obtener producto por ID",
        operation_description="Recupera la información completa de un producto existente mediante su ID.",
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_PATH,
                description="ID del producto que se desea consultar",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Producto obtenido correctamente",
                schema=ProductSerializer()
            ),
            404: openapi.Response(
                description="Producto no encontrado"
            ),
        },
    )
    def get(self, request, product_id):
        """Obtiene un producto por su ID."""
        product = self.service.get_product_by_id(product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary="Actualización parcial de un producto",
        operation_description=(
            "Permite modificar parcialmente los campos de un producto existente mediante su ID.\n\n"
            "Ejemplo de cuerpo JSON:\n"
            "```\n"
            "{\n"
            "  \"nombre\": \"actualizar nombre\",\n"
            "  \"precio\": 199.99\n"
            "}\n"
            "```"
        ),
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_PATH,
                description="ID del producto que se desea actualizar parcialmente",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        request_body=ProductUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Producto actualizado correctamente",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "El producto ha sido actualizado correctamente"
                    }
                }
            ),
            400: openapi.Response(
                description="Datos inválidos o error de validación"
            ),
            404: openapi.Response(
                description="Producto no encontrado"
            ),
        },
    )
    def patch(self, request, product_id):
        """Actualiza parcialmente un producto existente."""
        serializer = ProductUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated_product = self.service.update_product(product_id, serializer.validated_data)
            response_serializer = ProductSerializer(updated_product)
            return Response({
                "status": "success",
                "message": "El producto ha sido actualizado correctamente",
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Eliminar producto por ID",
        operation_description=(
            "Elimina un producto existente identificado por su ID.\n\n"
            "Ejemplo de uso:\n"
            "`DELETE /products/5/` eliminará el producto con ID 5."
        ),
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_PATH,
                description="ID del producto que se desea eliminar",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Producto eliminado correctamente",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "El producto con ID 5 ha sido eliminado correctamente."
                    }
                }
            ),
            404: openapi.Response(
                description="Producto no encontrado"
            ),
        },
    )
    def delete(self, request, product_id):
        """Elimina un producto por su ID."""
        self.service.delete_product(product_id)
        return Response(
            {
                "status": "success",
                "message": f"El producto con ID {product_id} ha sido eliminado correctamente."
            },
            status=status.HTTP_200_OK
        )