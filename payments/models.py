from django.db import models
from enum import Enum
import uuid
from django.conf import settings


class TransactionStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class PaymentMethod(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=50)
    # endpoint = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Modèle pour stocker toutes les transactions
    """
    reference = models.CharField(max_length=50, unique=True, editable=False)

    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='initiated_transactions',
        null=True
    )

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Montant de la transaction"
    )

    phone_number = models.CharField(
        max_length=20, help_text="Numéro de téléphone du client"
    )

    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        help_text="Méthode de paiement utilisée",
    )

    PAYMENT = "payment"
    DEPOSIT = "deposit"
    TRANSACTION_TYPES = [(PAYMENT, "Paiement"), (DEPOSIT, "Dépôt")]

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES,
        help_text="Type de transaction",
    )

    callback_url = models.URLField(
        null=True, blank=True, help_text="URL de callback pour les notifications"
    )

    status = models.CharField(
        max_length=20,
        choices=[(status.name, status.value) for status in TransactionStatus],
        default=TransactionStatus.PENDING.value,
        help_text="État actuel de la transaction",
    )

    # Référence retournée par le provider (MTN, Orange, etc.)
    provider_reference = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Référence donnée par le provider",
    )

    message = models.TextField(
        blank=True, help_text="Message pour le client/Détails de l'erreur"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = (
                f"ADS_{uuid.uuid4().hex[:12]}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.amount} FCFA ({self.status})"
