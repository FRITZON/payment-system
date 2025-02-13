from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les informations utilisateur."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "role", "is_active"]
        read_only_fields = ["id", "role", "is_active"]

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer pour valider la création d'un utilisateur."""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password"]
