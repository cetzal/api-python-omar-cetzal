from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import LoginSerializer, LogoutSerializer, TokenRefreshSerializer
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


class LogoutView(APIView):
    """
    Cierra la sesión de un usuario invalidando su token de actualización (refresh token).
    Endpoint: /auth/logout/
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    @swagger_auto_schema(
        operation_summary="Cerrar sesión (Logout)",
        operation_description=(
            "Finaliza la sesión del usuario invalidando su **refresh token**.\n\n"
            "Debe enviarse el token de actualización (`refresh`) obtenido durante el login.\n\n"
            "**Ejemplo de solicitud JSON:**\n"
            "```\n"
            "{\n"
            "  \"refresh\": \"<refresh_token>\"\n"
            "}\n"
            "```\n"
            "**Ejemplo de respuesta exitosa:**\n"
            "_Código 205 (Reset Content)_ — La sesión se ha cerrado correctamente.\n\n"
            "**Ejemplo de error:**\n"
            "```\n"
            "{\n"
            "  \"status\": \"error\",\n"
            "  \"message\": \"Token de actualización no válido\"\n"
            "}\n"
            "```"
        ),
        request_body=LogoutSerializer,
        responses={
            205: openapi.Response(
                description="Logout exitoso, el token de actualización fue invalidado",
            ),
            400: openapi.Response(
                description="Token inválido o error en la solicitud",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "Token de actualización no válido"
                    }
                }
            ),
        },
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data.get('refresh')

        try:
            success = self.service.logout_user(refresh_token)
            if success:
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"status":"error", "message": f"Token de actualización no válido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":"error", "message":f"Ha ocurrido un error inesperado durante el logout"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Permite obtener un nuevo access token a partir de un refresh token válido.
    Endpoint: /auth/refresh/token
    """
    @swagger_auto_schema(
        operation_summary="Actualizar token de acceso",
        operation_description=(
            "Actualiza el token de acceso usando un token de actualización válido.\n\n"
            "Devuelve un nuevo token de acceso si el token de actualización es válido."
        ),
        request_body=TokenRefreshSerializer,
        responses={
            200: openapi.Response(
                description="Token actualizado exitosamente",
                examples={
                    "application/json": {
                        "access": "<new_access_token>"
                    }
                },
            ),
            400: openapi.Response(description="Token de actualización inválido o expirado"),
            401: openapi.Response(description="Token inválido"),
        },
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response