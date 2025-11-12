from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer para la autenticación de usuarios.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_email(self, value):
        """
        Valida que el email no esté vacío.
        """
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_password(self, value):
        """
        Valida que la contraseña no esté vacía.
        """
        if not value:
            raise serializers.ValidationError("Password is required.")
        return value


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta de autenticación.
    """
    name = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class LogoutSerializer(serializers.Serializer):
    """
    Serializer para el cierre de sesión de usuarios.
    """
    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value):
        """
        Valida que el refresh token no esté vacío.
        """
        if not value:
            raise serializers.ValidationError("Refresh token is required.")
        return value


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer para la actualización de tokens.
    """
    refresh = serializers.CharField(required=True)

    def validate_refresh(self, value):
        """
        Valida que el refresh token no esté vacío.
        """
        if not value:
            raise serializers.ValidationError("Refresh token is required.")
        return value