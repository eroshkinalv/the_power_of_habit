import datetime

from celery import shared_task

from habit_tracker.models import Habit, DayChoices
from habit_tracker.services import send_tg_message


@shared_task
def check_done():
    """Снимает отметку, что действие выполнено."""

    habits = Habit.objects.filter(is_done=True)

    if habits:
        for habit in habits:
            habit.is_done = False
            habit.save()


@shared_task
def check_update():
    """Определяет не заброшена ли привычка и отпраляет сообщение, если действие не выполнялось более недели."""

    delta = datetime.timedelta(days=8)
    date = datetime.datetime.now().date() - delta

    habits = Habit.objects.filter(is_done=False, date_done=date)

    if habits:
        for habit in habits:
            message = f"Так не пойдет! Вы перестали работать над привычкой {habit.activity.lower()}."
            chat_id = habit.owner.tg_chat_id
            if chat_id:
                send_tg_message(chat_id, message)


@shared_task
def check_time():
    """Информирует о времени выполнения действия; сообщает, если выполнение действия было пропущено."""

    delta = datetime.timedelta(seconds=120)

    days_of_the_week = {
        0: DayChoices.objects.filter(days="Пн").first(),
        1: DayChoices.objects.filter(days="Вт").first(),
        2: DayChoices.objects.filter(days="Ср").first(),
        3: DayChoices.objects.filter(days="Чт").first(),
        4: DayChoices.objects.filter(days="Пт").first(),
        5: DayChoices.objects.filter(days="Сб").first(),
        6: DayChoices.objects.filter(days="Вс").first(),
    }

    current_day = datetime.datetime.now().date().weekday()
    day = days_of_the_week.get(current_day)

    date_time_info = datetime.datetime.now().time()
    current_time = date_time_info.strftime("%H:%M:00")
    habits = Habit.objects.filter(time=current_time, day_choice=day)

    date_time_warning = datetime.datetime.now() - delta
    warning_time = date_time_warning.strftime("%H:%M:00")
    habits_done = Habit.objects.filter(time=warning_time, day_choice=day, is_done=False)

    if habits:
        for habit in habits:
            message = f"Пришло время для того, чтобы {habit.activity.lower()}."
            chat_id = habit.owner.tg_chat_id
            if chat_id:
                send_tg_message(chat_id, message)

    if habits_done:
        for habit in habits_done:
            message = f"Кажется, Вы забыли, что собирались {habit.activity.lower()}."
            chat_id = habit.owner.tg_chat_id
            if chat_id:
                send_tg_message(chat_id, message)
