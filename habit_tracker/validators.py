from rest_framework.serializers import ValidationError

from habit_tracker.models import Habit


class HabitValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        bonus_habits = [habit.activity.lower() for habit in Habit.objects.filter(is_bonus=True)]

        linked_habit = dict(value).get(self.field)

        if linked_habit:

            if linked_habit.activity.lower() not in bonus_habits:
                raise ValidationError("К полезной привычке можно добавить только приятную привычку.")
