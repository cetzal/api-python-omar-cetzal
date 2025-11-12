from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from .repository import AuthRepository


class AuthService:
    """
    La clase AuthService encapsula la lógica empresarial para las operaciones de autenticación.
    """

    def __init__(self):
        self.repository = AuthRepository()

    def authenticate_user(self, email: str, password: str, request=None) -> dict:
        """
        Autentica un usuario con email y contraseña.

        Args:
            email (str): El email del usuario.
            password (str): La contraseña del usuario.
            request: El objeto de solicitud para señales.

        Returns:
            dict: Un diccionario con los detalles del usuario y tokens si la autenticación es exitosa.

        Raises:
            User.DoesNotExist: Si no se encuentra un usuario con el email proporcionado.
            ValueError: Si la contraseña es incorrecta.
        """
        user = self.repository.get_user_by_email(email)
        
        if not user.check_password(password):
            raise ValueError("La creadenciales son invalidas")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        user_details = {
            'name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

        if request:
            user_logged_in.send(sender=user.__class__, request=request, user=user)

        return user_details

    def logout_user(self, refresh_token: str) -> bool:
        """
        Invalidates a refresh token by blacklisting it.

        Args:
            refresh_token (str): The refresh token to blacklist.

        Returns:
            bool: True if the token was successfully blacklisted, False otherwise.
        """
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True
        except Exception:
            # If token is already blacklisted or invalid, return False
            return False