from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from habit_tracker.models import Habit

from users.models import User
from django.core.management import call_command

from users.permissions import IsUser


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="email@example.com", password="123zaq", phone="89111120303", tg_chat_id="123456789"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):

        url = reverse("users:user-list")
        data = {
            "email": "extramail@example.com",
            "password": "123zaq",
            "phone": "88002000600",
            "tg_chat_id": "987654321",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.all().count(), 2)

        call_command("add_user")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_update(self):

        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"phone": "81234567899"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("phone"), "81234567899")

    def test_user_delete(self):

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(User.objects.all().count(), 0)

    def test_user_list(self):

        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()

        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "password": self.user.password,
                "phone": self.user.phone,
                "image": None,
            }
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data, result)

    def test_user_name_is_email(self):
        user = User.objects.filter(id=self.user.pk).first()
        expected_user_name = user.email
        self.assertEqual(expected_user_name, str(user))


class PermissionsTestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create(
            email="email@example.com", password="123zaq", phone="89111120303", tg_chat_id="123456789"
        )
        self.user_2 = User.objects.create(
            email="extraemail@example.com", password="123zaq", phone="89111120303", tg_chat_id="123456789"
        )

        self.habit = Habit.objects.create(
            owner=self.user_1,
            location="home",
            time="21:00:00",
            activity="read a book",
            is_bonus=False,
            reward="milk and toast and honey",
            is_public=False,
        )
        self.another_habit = Habit.objects.create(
            owner=self.user_2,
            location="home",
            time="21:00:00",
            activity="write a diary entry",
            is_bonus=False,
            reward="sense of accomplishment",
            is_public=False,
            is_done=True,
            date_done="2025-01-01",
        )

        self.permission = IsUser()
        self.client.force_authenticate(user=self.user_1)

    def test_user_retrieve(self):

        url = reverse("users:user-detail", args=(self.user_2.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update(self):

        url = reverse("users:user-detail", args=(self.user_2.pk,))
        data = {"phone": "89998887766"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete(self):

        url = reverse("users:user-detail", args=(self.user_2.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_habit_update(self):

        url = reverse("habit_tracker:habit-detail", args=(self.habit.pk,))
        data = {"is_done": True, "date_done": "2024-01-01"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse("habit_tracker:habit-detail", args=(self.another_habit.pk,))
        data = {"is_done": True, "date_done": "2024-01-01"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
