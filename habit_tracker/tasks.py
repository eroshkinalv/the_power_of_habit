import datetime

from celery import shared_task

from habit_tracker.models import Habit
from habit_tracker.services import send_tg_message


@shared_task
def check_update():
    """Снимает отметку, что действие выполнено и определяет не заброшена ли привычка."""

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

    date_time_info = datetime.datetime.now().time()
    current_time = date_time_info.strftime("%H:%M:00")
    habits = Habit.objects.filter(time=current_time)

    date_time_warning = datetime.datetime.now() - delta
    warning_time = date_time_warning.strftime("%H:%M:00")
    habits_done = Habit.objects.filter(time=warning_time, is_done=False)

    if habits:
        for habit in habits:
            message = f"Пришло время для того, чтобы {habit.activity.lower()}."
            chat_id = habit.owner.tg_chat_id
            if chat_id:
                send_tg_message(chat_id, message)

    if habits_done:
        for habit in habits_done:
            message = f"Кажется, Вы забыли {habit.activity.lower()}."
            chat_id = habit.owner.tg_chat_id
            if chat_id:
                send_tg_message(chat_id, message)
