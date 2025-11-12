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

