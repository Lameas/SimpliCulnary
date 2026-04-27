from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="Numero de Telephone")
    adress = models.TextField(blank=True, verbose_name="Adresse")
    groups = models.ManyToManyField(
        Group,
        related_name="customer_groups",
        related_query_name="user",
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customer_permissions",
        related_query_name="user",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
