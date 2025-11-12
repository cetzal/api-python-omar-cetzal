from api.users.models import User
from django.core.exceptions import ObjectDoesNotExist


class AuthRepository:
    """
    La clase AuthRepository es responsable de todas las operaciones de la base de datos relacionadas con la autenticación.
    """

    @staticmethod
    def get_user_by_email(email: str) -> User:
        """
        Obtiene un usuario por su email.

        Args:
            email (str): El email del usuario.

        Returns:
            User: El objeto de usuario encontrado.

        Raises:
            User.DoesNotExist: Si no se encuentra un usuario con el email proporcionado.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise User.DoesNotExist(f"El recurso solicitado {email} no exist")