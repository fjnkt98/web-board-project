from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from boards.forms import PostForm
from boards.models import Board, Post, Topic


class Setup(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name="Django", description="Django board.")
        self.user = User.objects.create_user("john", "john@example.com", "complexpassword123")
        self.topic = Topic.objects.create(subject="Hello, world", board=self.board, starter=self.user)
        Post.objects.create(message="Lorem ipsum dolor sit amet", topic=self.topic, created_by=self.user)
        self.url = reverse("reply_topic", kwargs={"board_id": self.board.pk, "topic_id": self.topic.pk})


class TestReplyTopicLoginRequired(Setup):
    def test_redirection(self) -> None:
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")


class TestReplyTopicView(Setup):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username="john", password="complexpassword123")  # noqa: S106
        self.response = self.client.get(self.url)

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_csrf(self) -> None:
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self) -> None:
        form = self.response.context.get("form")
        self.assertIsInstance(form, PostForm)

        self.assertContains(self.response, "<input", 2)  # csrf and logout
        self.assertContains(self.response, "<textarea", 1)


class TestSuccessfulReply(Setup):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username="john", password="complexpassword123")  # noqa: S106
        self.response = self.client.post(self.url, {"message": "Hello, world!"})

    def test_redirection(self) -> None:
        self.assertRedirects(self.response, reverse("topic_posts", kwargs={"board_id": self.board.pk, "topic_id": self.topic.pk}))

    def test_reply_created(self) -> None:
        self.assertEqual(Post.objects.count(), 2)


class TestFailedReply(Setup):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username="john", password="complexpassword123")  # noqa: S106
        self.response = self.client.post(self.url, {})

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self) -> None:
        form = self.response.context.get("form")
        self.assertIsInstance(form, PostForm)
        self.assertTrue(bool(form.errors))  # type: ignore[union-attr]  # ty:ignore[unresolved-attribute]

    def test_reply_not_created(self) -> None:
        self.assertEqual(Post.objects.count(), 1)
