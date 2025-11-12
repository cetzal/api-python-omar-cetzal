from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer,UserUpdateSerializer
from .services import UserService

class UserListCreateAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'nombre',
                openapi.IN_QUERY,
                description="Filtrar usario por nombre (optional)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description="Filtrar usario por email (optional)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'activo',
                openapi.IN_QUERY,
                description="Filtrar usario por active status (optional)",
                type=openapi.TYPE_BOOLEAN
            ),
        ],
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        users = self.service.get_all_users(request.query_params)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "La peticion no a sido procesada"
        },
        operation_summary="Crear un nuevo usario",
        operation_description="Crea un nuevo usuario con los datos proporcionados."
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            created_user = self.service.create_user(serializer.validated_data)
            response_serializer = UserSerializer(created_user)
            return Response({
            "status": "success",
            "message": f"El usario se ha creado"
        }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateDestroyAPIView(APIView):
    """
    Metodos para interactuar con usario en especifico.
    Endpoint: /users/<int:user_id>/
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    @swagger_auto_schema(
        operation_summary="Obtener usuario por ID",
        operation_description="Devuelve la información detallada de un usuario específico.",
        responses={
            200: UserSerializer,
            404: openapi.Response(description="Usuario no encontrado")
        },
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="ID del usuario a consultar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
    )
    def get(self, request, user_id):
        """Obtiene un usuario por su ID."""
        user = self.service.get_user_by_id(user_id)
        if not user:
            return Response({"status": "error", "message": f"Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Actualizar usuario por ID",
        operation_description="Actualiza los datos de un usuario específico. Requiere todos los campos del serializer.",
        request_body=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
            400: openapi.Response(description="Errores de validación"),
            404: openapi.Response(description="Usuario no encontrado"),
        },
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="ID del usuario a actualizar",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
    )
    def put(self, request, user_id):
        """Actualiza completamente un usuario existente."""
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = self.service.update_user(user_id, serializer.validated_data)
            if not updated_user:
                return Response({"status": "error", "message": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
            response_serializer = UserSerializer(updated_user)
            return Response({"status": "succes", "message": f"El usuario ha sido actualizado"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

