from django.contrib.auth.models import User
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse

from boards.models import Board, Post, Topic


class Setup(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name="Django", description="Django board.")
        self.username = "john"
        self.password = "complexpassword123"  # noqa: S105
        self.user = User.objects.create_user(username=self.username, email="john@example.com", password=self.password)
        self.topic = Topic.objects.create(subject="Hello, world!", board=self.board, starter=self.user)
        self.post = Post.objects.create(message="This is a test post.", topic=self.topic, created_by=self.user)
        self.url = reverse(
            "edit_post",
            kwargs={
                "board_id": self.board.pk,
                "topic_id": self.topic.pk,
                "post_id": self.post.pk,
            },
        )


class TestEditPostViewLoginRequired(Setup):
    def test_redirection(self) -> None:
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")


class TestEditPostOtherUser(Setup):
    def setUp(self) -> None:
        super().setUp()
        user = User.objects.create_user(username="jane", email="jane@example.com", password="complexpassword123")  # noqa: S106
        self.client.login(username=user.get_username(), password="complexpassword123")  # noqa: S106
        self.response = self.client.get(self.url)

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 404)


class TestEditPostView(Setup):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.user.get_username(), password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self) -> None:
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self) -> None:
        form = self.response.context.get("form")
        self.assertIsNotNone(form)
        self.assertIsInstance(form, ModelForm)

        self.assertContains(self.response, "<input", 2)
        self.assertContains(self.response, "<textarea", 1)


class TestSuccessfulEditPost(Setup):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.user.get_username(), password=self.password)
        self.response = self.client.post(self.url, {"message": "edited message"})

    def test_redirection(self) -> None:
        topic_posts_url = reverse("topic_posts", kwargs={"board_id": self.board.pk, "topic_id": self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)

    def test_post_updated(self) -> None:
        self.post.refresh_from_db()
        self.assertEqual(self.post.message, "edited message")


class TestFailedEditPost(Setup):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.user.get_username(), password=self.password)
        self.response = self.client.post(self.url, {"message": ""})

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self) -> None:
        form = self.response.context.get("form")
        self.assertIsNotNone(form)
        self.assertTrue(bool(form.errors))  # ty:ignore[unresolved-attribute]
