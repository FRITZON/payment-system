from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import TransactionSerializer, PaymentMethodSerializer
from .services import PaymentService
from django.core.exceptions import ValidationError
from .models import PaymentMethod
from accounts.models import UserRole


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):

    user = request.user

    if user.role == UserRole.SUBSCRIBER:
        if not user.whitelisted_ips or request.META.get("REMOTE_ADDR") not in user.whitelisted_ips:
            return Response({"error": "IP non autorisée"}, status=403)
        
    if user.role == UserRole.CLIENT:
        if user.is_active:
            return Response({"error": "Compte inactif"}, status=403)

    serializer = TransactionSerializer(data=request.data)

    if serializer.is_valid():
        try:
            reference = serializer.validated_data["reference"]
            amount = serializer.validated_data["amount"]
            callback_url = serializer.validated_data.get("callback_url", "")
            phone_number = serializer.validated_data["phone_number"]
            payment_method_slug = serializer.validated_data["payment_method"]

            try:
                payment_method = PaymentMethod.objects.get(slug=payment_method_slug)
            except PaymentMethod.DoesNotExist:
                return Response(
                    {"detail": "Méthode de paiement invalide"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment_method_serializer = PaymentMethodSerializer(payment_method)

            payment_service = PaymentService()

            transaction = payment_service.initiate_payment(
                reference,
                amount,
                callback_url,
                phone_number,
                payment_method_slug,
                user=request.user,
            )

            return Response(
                {
                    "reference": transaction.reference,
                    "payment_method": payment_method_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
