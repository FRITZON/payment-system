from rest_framework import serializers
from .models import Transaction, PaymentMethod
from django.core.exceptions import ValidationError

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['slug', 'name', 'is_active']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['reference', 'amount', 'phone_number', 'payment_method', 'callback_url', 'status']

    def validate_amount(self, value):
        if value <= 99:
            raise serializers.ValidationError("Le montant doit être au moins de 100 Fcfa")
        return value
    
    def validate_payment_method(self, value):
        try:
            payment_method = PaymentMethod.objects.get(slug=value)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Méthode de paiement invalide")
        return payment_method