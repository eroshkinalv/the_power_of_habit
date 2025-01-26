import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habit_tracker.filters import IsPublicFilterBackend
from habit_tracker.models import Habit, DayChoices
from habit_tracker.paginators import HabitPagination
from habit_tracker.serializers import HabitSerializer, DaySerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    filter_backends = (IsPublicFilterBackend,)
    filterset_fields = ("owner", "is_public")

    def get_permissions(self):

        if self.action in ["retrieve", "update", "destroy", "partial_update", "create"]:
            self.permission_classes = (IsOwner,)

        elif self.action in [
            "list",
        ]:
            self.permission_classes = (IsAuthenticated,)

        return super().get_permissions()

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)

        habit = serializer.save()

        if not habit.day_choice.all():
            habit.day_choice.set((day.id for day in DayChoices.objects.all()))

        if habit.is_bonus is True:
            habit.linked_habit = None
            habit.reward = None

        elif habit.is_bonus is False:
            bonus_habit = Habit.objects.filter(is_bonus=True, activity=habit.linked_habit).first()

            if bonus_habit:
                if habit.linked_habit == bonus_habit.activity:
                    bonus_habit.day_choice.set(habit.day_choice.all())
                    bonus_habit.save()

        habit.save()

    def perform_update(self, serializer):
        habit = serializer.save()
        if habit.is_done is True:
            habit.date_done = datetime.datetime.now().date()


class DayViewSet(ModelViewSet):

    queryset = DayChoices.objects.all()
    serializer_class = DaySerializer
