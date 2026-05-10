from django.test import TestCase
from django.urls import reverse


class TestPasswordResetDoneView(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse("password_reset_done"))

    def test_password_reset_done_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)
