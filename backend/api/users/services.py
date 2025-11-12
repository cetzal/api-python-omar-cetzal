from .repository import UserRepository

class UserService:
    """
    La clase UserService encapsula la lógica empresarial para las operaciones del usuario. 
    Actúa como intermediario entre la capa de presentación (vistas) y la capa de acceso a datos (repositorio), 
    que organiza los pasos necesarios para cumplir un caso de uso.
    """

    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self, filters=None):
        """Obtener todo los usarios"""
        return self.repository.get_all_users(filters)
    
    def create_user(self, validated_data):
        """
        funcion encarga de regitrar usario o validaciones necesarios
        """
        return self.repository.create_user(validated_data)

