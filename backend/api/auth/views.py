from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import LoginSerializer
from .services import AuthService
from django.core.exceptions import ObjectDoesNotExist


class LoginView(APIView):
    """
    Endpoint de autenticación de usuarios.
    Permite iniciar sesión con email y contraseña y devuelve los tokens JWT.
    """

    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    @swagger_auto_schema(
        operation_summary="Inicio de sesión de usuario (Login)",
        operation_description=(
            "Autentica al usuario mediante su **email** y **contraseña**.\n\n"
            "Si las credenciales son válidas, devuelve los tokens JWT de acceso y actualización.\n\n"
        ),
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Inicio de sesión exitoso, devuelve los tokens JWT",
                examples={
                    "application/json": {
                        "name": "Juan Pérez",
                        "access": "<access_token>",
                        "refresh": "<refresh_token>"
                    }
                },
            ),
            400: openapi.Response(description="Datos inválidos o faltantes"),
            401: openapi.Response(description="Credenciales incorrectas"),
            403: openapi.Response(description="Cuenta desactivada"),
            500: openapi.Response(description="Error interno en el servidor"),
        },
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        try:
            user_data = self.service.authenticate_user(email, password, request)
            return Response(user_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"status":"error", "message": f"Credenciales invalidas"}, status=status.HTTP_401_UNAUTHORIZED)
        except ValueError:
            return Response({"status":"error", "message": f"No se puede autenticar con las credenciales proporcionadas o la cuenta ha sido desactivada"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"status":"error", "message": f"Ha ocurrido un error inesperado"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

