# Generated by Django 5.1.4 on 2025-01-26 12:57

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DayChoices",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("days", models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Habit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Место, в котором необходимо выполнять привычку",
                        max_length=100,
                        null=True,
                        verbose_name="Место",
                    ),
                ),
                (
                    "time",
                    models.TimeField(help_text="Время, когда необходимо выполнять привычку", verbose_name="Время"),
                ),
                (
                    "activity",
                    models.CharField(
                        help_text="Действие, которое представляет собой привычка",
                        max_length=200,
                        verbose_name="Действие",
                    ),
                ),
                (
                    "is_bonus",
                    models.BooleanField(
                        default=False,
                        help_text="Привычка, которую можно привязать к выполнению полезной привычки",
                        verbose_name="Приятная привычка",
                    ),
                ),
                (
                    "linked_habit",
                    models.CharField(
                        blank=True,
                        help_text="Привычка, которая связана с другой привычкой",
                        max_length=200,
                        null=True,
                        verbose_name="Связанная привычка",
                    ),
                ),
                (
                    "reward",
                    models.CharField(
                        blank=True,
                        help_text="Чем пользователь должен себя вознаградить после выполнения",
                        max_length=200,
                        null=True,
                        verbose_name="Вознаграждение ",
                    ),
                ),
                (
                    "time_to_complete",
                    models.DurationField(
                        default=datetime.timedelta(seconds=120),
                        help_text="Время, которое пользователь предположительно потратит "
                                  "на то чтобы приступить к выполнению",
                        verbose_name="Время на выполнение (в секундах)",
                    ),
                ),
                (
                    "is_public",
                    models.BooleanField(
                        default=False,
                        help_text="Привычка, которую могут видеть другие пользователи",
                        verbose_name="Видно всем",
                    ),
                ),
                ("is_done", models.BooleanField(default=False, verbose_name="Выполнено")),
                ("date_done", models.DateField(blank=True, null=True, verbose_name="Дата выполнения действия")),
                (
                    "day_choice",
                    models.ManyToManyField(
                        related_name="day_choice",
                        to="habit_tracker.daychoices",
                        verbose_name="Дни выполнения действия",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        help_text="Создатель привычки",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Привычка",
                "verbose_name_plural": "Привычки",
            },
        ),
    ]
