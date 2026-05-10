from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.forms import SignupForm


class TestSignup(TestCase):
    def setUp(self) -> None:
        self.response = self.client.get(reverse("signup"))

    def test_signup_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self) -> None:
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self) -> None:
        form = self.response.context.get("form")
        self.assertIsInstance(form, SignupForm)

        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class TestSuccessfulSignup(TestCase):
    def setUp(self) -> None:
        self.response = self.client.post(
            reverse("signup"),
            data={
                "username": "john",
                "email": "john@example.com",
                "password1": "complexpassword123",
                "password2": "complexpassword123",
            },
        )

    def test_redirection(self) -> None:
        self.assertRedirects(self.response, reverse("home"))

    def test_user_created(self) -> None:
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self) -> None:
        response = self.client.get(reverse("home"))
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)  # ty:ignore[unresolved-attribute]


class TestFailedSignup(TestCase):
    def setUp(self) -> None:
        self.response = self.client.post(reverse("signup"), data={})

    def test_signup_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self) -> None:
        form = self.response.context.get("form")
        self.assertTrue(form.errors)  # ty:ignore[unresolved-attribute]

    def test_user_not_created(self) -> None:
        self.assertFalse(User.objects.exists())
