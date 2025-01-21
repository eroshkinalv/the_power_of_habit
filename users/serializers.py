from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from habit_tracker.models import Habit
from users.models import User


class UserSerializer(ModelSerializer):

    habits = SerializerMethodField(read_only=True)

    def get_habits(self, user):
        return [habit.activity for habit in Habit.objects.filter(owner=user)]

    public_habits = SerializerMethodField(read_only=True)

    def get_public_habits(self, user):
        return [habit.activity for habit in Habit.objects.filter(owner=user, is_public=True)]

    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "image", "habits", "public_habits")
