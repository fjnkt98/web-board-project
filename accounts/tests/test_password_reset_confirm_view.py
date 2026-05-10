from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TestPasswordResetConfirmView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user("john", "john@example.com", "complexpassword123")

        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        self.response = self.client.get(
            reverse("password_reset_confirm", kwargs={"uidb64": self.uid, "token": self.token}),
            follow=True,
        )

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self) -> None:
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self) -> None:
        form = self.response.context.get("form")
        self.assertIsInstance(form, SetPasswordForm)

        self.assertContains(self.response, "<input", 3)
        self.assertContains(self.response, 'type="password"', 2)


class TestInvalidPasswordResetConfirmView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user("john", "john@example.com", "complexpassword123")

        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        user.set_password("anotherpassword123")
        user.save()

        self.response = self.client.get(
            reverse("password_reset_confirm", kwargs={"uidb64": self.uid, "token": self.token}),
            follow=True,
        )

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_html(self) -> None:

        self.assertContains(self.response, "invalid password reset link")
        self.assertContains(self.response, f'href="{reverse("password_reset")}"')
