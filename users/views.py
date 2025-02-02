from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)

    def get_permissions(self):

        if self.action == "create":
            self.permission_classes = (AllowAny,)

        return super().get_permissions()

    def perform_create(self, serializer):

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
