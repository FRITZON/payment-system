from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Administrateur"
    OPERATOR = "OPERATOR", "Opérateur"
    CLIENT = "CLIENT", "Client"
    SUBSCRIBER = "SUBSCRIBER", "Abonné API"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CLIENT,
        help_text="Rôle de l'utilisateur dans le système",
    )

    phone_number = models.CharField(
        max_length=20, blank=True, help_text="Numéro de téléphone de l'utilisateur"
    )

    # Pour les abonnés API
    api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        help_text="Clé API pour les abonnés",
    )

    whitelisted_ips = models.JSONField(
        default=list, blank=True, help_text="Liste des IPs autorisées"
    )

    is_active = models.BooleanField(
        default=True, help_text="Indique si l'utilisateur est actif"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role()})"

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_operator(self):
        return self.role == UserRole.OPERATOR

    @property
    def is_subscriber(self):
        return self.role == UserRole.SUBSCRIBER
    
    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def generate_api_key(self):
        """Génère une nouvelle clé API pour les abonnés."""
        if self.is_subscriber:
            self.api_key = get_random_string(40)
            self.save()
            return self.api_key
        raise ValueError("Seuls les abonnés API peuvent avoir une clé API.")

    def __str__(self):
        return f"{self.username} {self.role}"
