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
        funcion que se encarga de regitrar usario o/y validaciones necesarios
        """
        return self.repository.create_user(validated_data)
    
    def get_user_by_id(self, user_id):
        return self.repository.get_user_by_id(user_id)

    def update_user(self, user_id, validated_data):
        user_instance = self.repository.get_user_by_id(user_id)
        return self.repository.update_user(user_instance, validated_data)

    def delete_user(self, user_id):
        user_instance = self.repository.get_user_by_id(user_id)
        self.repository.delete_user(user_instance)

