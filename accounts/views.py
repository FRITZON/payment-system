from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsAdmin


class UserCreateView(generics.CreateAPIView):

    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            phone_number=serializer.validated_data.get("phone_number", ""),
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "message": "Utilisateur créé avec succès",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role.Admin:
            return User.objects.all()
        return User.objects.filter(
            id=user.id
        )  # Un utilisateur ne peut voir que lui-même.


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return User.objects.all()
        return User.objects.filter(
            id=user.id
        )  # Un utilisateur ne peut modifier que lui-même.


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


@api_view(["PATCH"])
@permission_classes([IsAdmin])
def deactivate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.deactivate()
        return Response({"message": "Utilisateur désactivé"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé"}, status=404)


@api_view(["PATCH"])
@permission_classes([IsAdmin])
def activate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.activate()
        return Response({"message": "Utilisateur activé"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé"}, status=404)


@api_view(["POST"])
@permission_classes([IsAdmin])
def generate_api_key(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        api_key = user.generate_api_key()
        return Response({"api_key": api_key}, status=200)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé"}, status=404)
