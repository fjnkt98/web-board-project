from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestPasswordChangeViewAnonymousUser(TestCase):
    def test_redirection(self) -> None:
        url = reverse("password_change")
        self.response = self.client.get(url)
        self.assertRedirects(self.response, f"{reverse('login')}?next={url}")


class TestPasswordChangeViewAuthenticatedUser(TestCase):
    def setup_user(self, data: dict | None = None) -> None:
        self.user = User.objects.create_user("john", "john@example.com", "complexpassword123")
        self.url = reverse("password_change")
        self.client.login(username="john", password="complexpassword123")  # noqa: S106
        self.response = self.client.post(self.url, data or {})


class TestSuccessfulPasswordChange(TestPasswordChangeViewAuthenticatedUser):
    def setUp(self) -> None:
        self.setup_user(
            data={
                "old_password": "complexpassword123",
                "new_password1": "newcomplexpassword123",
                "new_password2": "newcomplexpassword123",
            }
        )

    def test_redirection(self) -> None:
        self.assertRedirects(self.response, reverse("password_change_done"))

    def test_password_changed(self) -> None:
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newcomplexpassword123"))

    def test_user_authentication(self) -> None:
        response = self.client.get(reverse("home"))
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)  # ty:ignore[unresolved-attribute]


class TestFailedPasswordChange(TestPasswordChangeViewAuthenticatedUser):
    def setUp(self) -> None:
        self.setup_user(data={})

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)  # ty:ignore[unresolved-attribute]

    def test_password_unchanged(self) -> None:
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("complexpassword123"))
