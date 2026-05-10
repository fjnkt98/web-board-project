from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TestPasswordResetView(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse("password_reset"))

    def test_password_reset_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self) -> None:
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self) -> None:
        form = self.response.context.get("form")
        self.assertIsInstance(form, PasswordResetForm)

        self.assertContains(self.response, "<input", 2)
        self.assertContains(self.response, 'type="email"', 1)


class TestSuccessfulPasswordReset(TestCase):
    def setUp(self) -> None:
        email = "john@example.com"
        User.objects.create_user("john", email, "complexpassword123")
        self.response = self.client.post(reverse("password_reset"), data={"email": email})

    def test_redirection(self) -> None:
        self.assertRedirects(self.response, reverse("password_reset_done"))

    def test_send_password_reset_email(self) -> None:
        self.assertEqual(1, len(mail.outbox))


class TestFailedPasswordReset(TestCase):
    def setUp(self) -> None:
        self.response = self.client.post(reverse("password_reset"), data={"email": "donotexist@example.com"})

    def test_redirection(self) -> None:
        self.assertRedirects(self.response, reverse("password_reset_done"))

    def test_no_email_sent(self) -> None:
        self.assertEqual(0, len(mail.outbox))
