import datetime

from rest_framework.serializers import ValidationError

from habit_tracker.models import Habit


class TimeToCompleteValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        time_to_complete = dict(value).get(self.field)

        if time_to_complete:
            time = datetime.timedelta(seconds=120)

            if time_to_complete > time:
                raise ValidationError("Время выполнения привычки не должно превышать 120 секунд.")


class HabitValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):

        habits = [habit.activity.lower() for habit in Habit.objects.filter(is_bonus=False)]
        bonus_habits = [habit.activity.lower() for habit in Habit.objects.filter(is_bonus=True)]

        linked_habit = dict(value).get(self.field)

        if linked_habit:

            if linked_habit.lower() in habits:
                raise ValidationError("К полезной привычке можно добавить только приятную привычку.")

            elif linked_habit.lower() not in bonus_habits:
                raise ValidationError("Сначала создайте приятную привычку. Связанную привычку можно указать для полезных привычек, но не для приятных.")
