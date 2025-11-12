from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Maneja la validación y transformación de datos de usuario entre la API (JSON)
    """
    nombre = serializers.CharField(source='first_name')
    apellido = serializers.CharField(source='last_name')
    edad = serializers.IntegerField(source='age', required=False, allow_null=True)
    activo = serializers.BooleanField(source='is_active', default=True)
    created = serializers.DateTimeField(source='created_at', read_only=True)


    class Meta:
        model = User
        # Los campos que se incluirán en la representación de la API.
        fields = [
            'id',
            'username',
            'nombre',
            'apellido',
            'email',
            'edad',
            'activo',
            'created',
            'last_update',
            'password',
        ]
        extra_kwargs = {
            # campos de solo escritura.
            'password': {'write_only': True},
            # forzando campos requerido para el api
            'email': {'required': True},
        }

class UserUpdateSerializer(UserSerializer):
    """
    Serializer para actualización de usuarios (PUT/PATCH).
    Hereda de UserSerializer pero hace opcional los campos.
    """
    class Meta(UserSerializer.Meta):
        extra_kwargs = {
            **UserSerializer.Meta.extra_kwargs,
            'password': {'write_only': True, 'required': False},  
            'email': {'required': False},  
        }