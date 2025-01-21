import datetime

from django.db import models

from users.models import User


class Habit(models.Model):

    owner = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, help_text="Создатель привычки")
    location = models.CharField(max_length=100, verbose_name="Место", blank=True, null=True, help_text="Место, в котором необходимо выполнять привычку")
    time = models.TimeField(verbose_name="Время", help_text="Время, когда необходимо выполнять привычку")
    activity = models.CharField(max_length=200, verbose_name="Действие", help_text="Действие, которое представляет собой привычка")

    # is_bonus - булевое поле, которые указывает на то, что привычка является приятной, а не полезной
    is_bonus = models.BooleanField(default=False, verbose_name="Признак приятной привычки", help_text="Привычка, которую можно привязать к выполнению полезной привычки")
    # linked_habit важно указывать для полезных привычек, но не для приятных.
    linked_habit = models.CharField(max_length=200, verbose_name="Связанная привычка", blank=True, null=True, help_text="Привычка, которая связана с другой привычкой")

    RECURRING_CHOICES = (("Ежедневно", "Ежедневно"), ("Один раз в неделю", "Один раз в неделю"), ("Два раза в неделю", "Два раза в неделю"), ("Три раза в неделю", "Три раза в неделю"))
    recurring = models.CharField(max_length=250, verbose_name="Периодичность", choices=RECURRING_CHOICES, blank=True, null=True, default="Ежедневно")

    reward = models.CharField(max_length=200, verbose_name="Вознаграждение ", blank=True, null=True, help_text="Чем пользователь должен себя вознаградить после выполнения")
    time_to_complete = models.DurationField(default=datetime.timedelta(seconds=120), verbose_name="Время на выполнение (в секундах)", help_text="Время, которое пользователь предположительно потратит на то чтобы приступить к выполнению")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    is_done = models.BooleanField(default=False, verbose_name="Выполнено")
    date_done = models.DateField(verbose_name="Дата выполнения действия", blank=True, null=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __int__(self):
        return self.activity
