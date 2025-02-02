from django.core.management.base import BaseCommand

from habit_tracker.models import DayChoices


class Command(BaseCommand):
    help = "Добавьте дни недели"

    def handle(self, *args, **kwargs):

        day_choices = DayChoices.objects.all()

        week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

        for day in week:

            if not day_choices.filter(days=day):
                day_choices.days = day
                DayChoices.objects.create(days=day)
