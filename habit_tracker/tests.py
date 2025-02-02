import requests
from django.core.management import call_command

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN
from habit_tracker.models import Habit, DayChoices
from habit_tracker.services import send_tg_message
from habit_tracker.tasks import check_done, check_update, check_time
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="email@example.com", password="123zaq", phone="89111120303", tg_chat_id="123456789"
        )
        self.habit = Habit.objects.create(
            owner=self.user,
            location="home",
            time="21:00:00",
            activity="read a book",
            is_bonus=False,
            reward="milk and toast and honey",
            is_public=False,
        )
        self.another_habit = Habit.objects.create(
            owner=self.user,
            location="home",
            time="21:00:00",
            activity="write a diary entry",
            is_bonus=False,
            reward="sense of accomplishment",
            is_public=False,
            is_done=True,
            date_done="2025-01-01",
        )
        self.bonus_habit = Habit.objects.create(
            owner=self.user, location="home", time="22:00:00", activity="meditate", is_bonus=True, is_public=False
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):

        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("activity"), self.habit.activity)

    def test_habit_create(self):

        url = reverse("habit_tracker:habit-list")
        data = {
            "owner": self.user,
            "location": "home",
            "time": "07:00:00",
            "activity": "do morning exercises",
            "linked_habit": self.bonus_habit.pk,
            "is_bonus": False,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Habit.objects.all().count(), 4)

        url = reverse("habit_tracker:habit-list")
        data = {
            "owner": self.user,
            "location": "home",
            "time": "08:00:00",
            "activity": "eat an apple a day",
            "is_bonus": True,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Habit.objects.all().count(), 5)

    def test_habit_exception(self):

        url = reverse("habit_tracker:habit-list")
        data = {
            "owner": self.user,
            "location": "home",
            "time": "08:00:00",
            "activity": "eat an apple a day",
            "is_bonus": True,
            "reward": "chocolate",
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        data = {
            "owner": self.user,
            "location": "home",
            "time": "08:00:00",
            "activity": "eat an apple a day",
            "linked_habit": "keeps a doctor away",
            "is_bonus": True,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        data = {
            "owner": self.user,
            "location": "home",
            "time": "21:00:00",
            "activity": "read a book",
            "linked_habit": "write plans for the next day",
            "is_bonus": False,
            "is_public": False,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        data = {
            "owner": self.user,
            "location": "home",
            "time": "21:00:00",
            "activity": "read a book",
            "linked_habit": "meditate",
            "reward": "chocolate",
            "is_bonus": False,
            "is_public": False,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        data = {
            "owner": self.user,
            "location": "home",
            "time": "08:00:00",
            "activity": "eat an apple a day",
            "is_bonus": False,
            "is_public": False,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

        data = {
            "owner": self.user,
            "location": "home",
            "time": "08:00:00",
            "activity": "eat an apple a day",
            "is_bonus": False,
            "linked_habit": "write a diary entry",
            "is_public": False,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertRaises(ValidationError)

    def test_habit_update(self):

        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        data = {"is_done": True, "date_done": "2024-01-01"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("is_done"), True)
        self.assertEqual(data.get("date_done"), "2024-01-01")

    def test_habit_delete(self):

        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):

        url = reverse("habit_tracker:habit-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "location": self.habit.location,
                    "time": self.habit.time,
                    "activity": self.habit.activity,
                    "is_bonus": self.habit.is_bonus,
                    "linked_habit": self.habit.linked_habit,
                    "reward": self.habit.reward,
                    "time_to_complete": "00:02:00",
                    "is_public": self.habit.is_public,
                    "is_done": self.habit.is_done,
                    "date_done": self.habit.date_done,
                    "owner": self.user.pk,
                    "day_choice": [],
                },
                {
                    "id": self.another_habit.pk,
                    "location": self.another_habit.location,
                    "time": self.another_habit.time,
                    "activity": self.another_habit.activity,
                    "is_bonus": self.another_habit.is_bonus,
                    "linked_habit": self.another_habit.linked_habit,
                    "reward": self.another_habit.reward,
                    "time_to_complete": "00:02:00",
                    "is_public": self.another_habit.is_public,
                    "is_done": self.another_habit.is_done,
                    "date_done": self.another_habit.date_done,
                    "owner": self.user.pk,
                    "day_choice": [],
                },
                {
                    "id": self.bonus_habit.pk,
                    "location": self.bonus_habit.location,
                    "time": self.bonus_habit.time,
                    "activity": self.bonus_habit.activity,
                    "is_bonus": self.bonus_habit.is_bonus,
                    "linked_habit": self.bonus_habit.linked_habit,
                    "reward": self.bonus_habit.reward,
                    "time_to_complete": "00:02:00",
                    "is_public": self.bonus_habit.is_public,
                    "is_done": self.bonus_habit.is_public,
                    "date_done": self.bonus_habit.date_done,
                    "owner": self.user.pk,
                    "day_choice": [],
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)

    def test_habit_is_activity(self):
        habit = Habit.objects.filter(id=self.habit.pk).first()
        expected_habit = habit.activity
        self.assertEqual(expected_habit, str(habit))

    def test_send_tg_message_error(self):

        params = {"text": "Ok", "chat_id": self.user.tg_chat_id}

        response = requests.get(f"{TELEGRAM_URL}12345678912345679/sendMessage", params=params)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_send_tg_message(self):

        func = send_tg_message(self.user.tg_chat_id, "OK")
        self.assertEqual(func, None)

    def test_celery_task_check_done(self):

        url = reverse("habit_tracker:habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Habit.objects.filter(is_done=False).count(), 2)

        check_done()

        self.assertEqual(Habit.objects.filter(is_done=False).count(), 3)

        check_update()

        func = check_update()
        self.assertEqual(func, None)

        check_time()

        func = check_time()
        self.assertEqual(func, None)


class DaysTestCase(APITestCase):

    def setUp(self):
        self.day = DayChoices.objects.create(days="Пн")
        self.user = User.objects.create(
            email="email@example.com", password="123zaq", phone="89111120303", tg_chat_id="123456789"
        )
        self.client.force_authenticate(user=self.user)

    def test_days_retrieve(self):

        url = reverse("habit_tracker:day-detail", args=(self.day.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("days"), self.day.days)

    def test_days_create(self):

        url = reverse("habit_tracker:day-list")
        data = {"days": "Вт"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(DayChoices.objects.all().count(), 2)

        call_command("add_days")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_days_update(self):

        url = reverse("habit_tracker:day-detail", args=(self.day.pk,))
        data = {"days": "Mon"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("days"), "Mon")

    def test_days_delete(self):

        url = reverse("habit_tracker:day-detail", args=(self.day.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(DayChoices.objects.all().count(), 0)

    def test_user_list(self):

        url = reverse("habit_tracker:day-list")
        response = self.client.get(url)
        data = response.json()

        result = [{"id": self.day.pk, "days": self.day.days}]

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)

    def test_day_choices_name_is_day(self):
        day = DayChoices.objects.filter(id=self.day.pk).first()
        expected_day = day.days
        self.assertEqual(expected_day, str(day))
