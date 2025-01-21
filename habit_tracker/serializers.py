from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from habit_tracker.models import Habit
from habit_tracker.validators import TimeToCompleteValidator, HabitValidator


class HabitSerializer(ModelSerializer):

    def validate(self, attrs):

        linked_habit = attrs.get('linked_habit')
        reward = attrs.get('reward')

        if attrs.get('is_bonus') is False:
            if linked_habit:
                if reward:
                    raise ValidationError("Невозможно одновременно установить связанную привычку и вознаграждение. Можно заполнить только одно из двух полей.")

            if not linked_habit:
                if not reward:
                    raise ValidationError("Необходимо установить связанную привычку или вознаграждение. Можно заполнить только одно из двух полей.")
        else:
            if reward:
                raise ValidationError("Не указывается для приятных привычек.")

        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["owner", "time_to_complete"]
        validators = [TimeToCompleteValidator(field="time_to_complete"), HabitValidator(field="linked_habit")]
