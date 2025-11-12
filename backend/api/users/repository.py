from django.shortcuts import get_object_or_404
from .models import User

class UserRepository:
    """
    La clase UserRepository es responsable de todas las operaciones de la base de datos relacionado con el modelo de Usuario.
    """

    def get_all_users(self, filters=None):
        queryset = User.objects.all()
        if filters:
            if 'username' in filters:
                queryset = queryset.filter(username__icontains=filters['username'])

            if 'nombre' in filters:
                queryset = queryset.filter(first_name__icontains=filters['nombre'])
            
            if 'email' in filters:
                queryset = queryset.filter(email__icontains=filters['email'])

            if 'edad' in filters:
                try:
                    edad_val = int(filters['edad'])
                    queryset = queryset.filter(age=edad_val)
                except (ValueError, TypeError):
                    pass

            if 'activo' in filters:
                is_active_val = str(filters.get('activo', '')).lower() in ['true', '1', 'yes']
                queryset = queryset.filter(is_active=is_active_val)
            
        return queryset.order_by('id')

    def create_user(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_user_by_id(self, user_id):
        return get_object_or_404(User, id=user_id)

    def update_user(self, user, validated_data):
        password = validated_data.pop('password', None)

        user.username = validated_data.get('username', user.username)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.age = validated_data.get('age', user.age)
        
        if password:
            user.set_password(password)
            
        user.save()
        return user

    def delete_user(self, user):
        user.delete()
