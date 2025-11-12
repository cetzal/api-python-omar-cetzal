from .repository import ProductRepository

class ProductService:
    """
    La clase ProductService encapsula la lógica empresarial para las operaciones del producto.
    Actúa como intermediario entre la capa de presentación (vistas) y la capa de acceso a datos (repositorio),
    que organiza los pasos necesarios para cumplir un caso de uso.
    """

    def __init__(self):
        self.repository = ProductRepository()

    def get_all_products(self, filters=None):
        return self.repository.get_all_products(filters)

    def create_product(self, validated_data):
        return self.repository.create_product(validated_data)

    def get_product_by_id(self, product_id):
        return self.repository.get_product_by_id(product_id)

    def update_product(self, product_id, validated_data):
        product_instance = self.repository.get_product_by_id(product_id)
        return self.repository.update_product(product_instance, validated_data)

    def delete_product(self, product_id):
        product_instance = self.repository.get_product_by_id(product_id)
        self.repository.delete_product(product_instance)