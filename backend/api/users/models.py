from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    se usara la tabla sabe que proporciona djando y solo se agrega los campos faltantes
    """
    age = models.PositiveIntegerField(verbose_name="Edad", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    # se puede agrega mas campos si se requiere

    def __str__(self):
        return self.username