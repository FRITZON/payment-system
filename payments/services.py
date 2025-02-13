from django.core.exceptions import ValidationError
from providers.mtn.services import MTNMomoService
from .models import Transaction, PaymentMethod, TransactionStatus

class PaymentService:
    def __init__(self):
        self.mtn_service = MTNMomoService()

    def initiate_payment(self, reference, amount, callback_url, phone_number, payment_method_slug, user):
        try:
            payment_method = PaymentMethod.objects.get(slug=payment_method_slug)
        except PaymentMethod.DoesNotExist:
            raise ValidationError("Méthode de paiement invalide")
        
        payment_method = PaymentMethod.objects.get(slug=payment_method_slug)
        
        transaction = Transaction()
        
        transaction.reference = reference
        transaction.amount = amount
        transaction.phone_number = phone_number
        transaction.payment_method = payment_method
        transaction.callback_url = callback_url
        transaction.initiated_by = user
        transaction.status = TransactionStatus.PENDING.value

        transaction.save()

        if payment_method_slug == "mtn":
            self.mtn_service.request_payment(transaction)

        return transaction
           