from django.test import TestCase
from django.urls import reverse


class TestPasswordResetCompleteView(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse("password_reset_complete"))

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)
