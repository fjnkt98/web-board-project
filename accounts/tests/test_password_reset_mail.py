from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TestPasswordResetMail(TestCase):
    def setUp(self) -> None:
        User.objects.create_user("john", "john@example.com", "complexpassword123")
        self.response = self.client.post(reverse("password_reset"), data={"email": "john@example.com"})
        self.email = mail.outbox[0]

    def test_email_subject(self) -> None:
        self.assertEqual("[Boards] Please reset your password", self.email.subject)

    def test_email_body(self) -> None:
        context = self.response.context
        token = context.get("token")
        uid = context.get("uid")
        password_reset_token_url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn("john", self.email.body)
        self.assertIn("john@example.com", self.email.body)

    def test_email_to(self) -> None:
        self.assertEqual(["john@example.com"], self.email.to)
