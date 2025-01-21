import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habit_tracker.filters import IsOwnerFilterBackend, IsPublicFilterBackend
from habit_tracker.models import Habit
from habit_tracker.paginators import HabitPagination
from habit_tracker.serializers import HabitSerializer
from users.permissions import IsOwnerOrReadOnly, IsOwner


class HabitViewSet(ModelViewSet):

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    filter_backends = [IsOwnerFilterBackend, IsPublicFilterBackend]
    filterset_fields = ("owner", "is_public")
    permission_classes = (IsOwnerOrReadOnly,)

    def get_permissions(self):

        if self.action in ["retrieve", "update", "destroy", "partial_update", "create"]:
            self.permission_classes = (IsOwner,)
            self.filter_backends = (IsOwnerFilterBackend,)

        elif self.action in ["list",]:
            self.permission_classes = (IsAuthenticated,)
            self.filter_backends = (IsPublicFilterBackend,)

        return super().get_permissions()

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)

        habit = serializer.save()

        if habit.is_bonus is True:
            habit.linked_habit = None
            habit.reward = None
            habit.recurring = None

        elif habit.is_bonus is False:
            bonus_habit = Habit.objects.filter(is_bonus=True, activity=habit.linked_habit).first()

            if bonus_habit:
                if habit.linked_habit == bonus_habit.activity:
                    bonus_habit.recurring = habit.recurring
                    bonus_habit.save()

        habit.save()

    def perform_update(self, serializer):
        habit = serializer.save()
        if habit.is_done is True:
            habit.date_done = datetime.datetime.now().date()


