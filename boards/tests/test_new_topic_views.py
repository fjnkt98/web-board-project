from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from boards.forms import NewTopicForm
from boards.models import Board, Post, Topic


class TestNewTopic(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name="Django", description="Django board.")
        User.objects.create_user("testuser", "test@example.com", "testpassword")
        self.client.login(username="testuser", password="testpassword")  # noqa: S106

    def test_new_topic_views_success_status_code(self) -> None:
        response = self.client.get(reverse("new_topic", kwargs={"board_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self) -> None:
        response = self.client.get(reverse("new_topic", kwargs={"board_id": 2}))
        self.assertEqual(response.status_code, 404)

    def test_new_topic_view_contains_navigation_links(self) -> None:
        response = self.client.get(reverse("new_topic", kwargs={"board_id": 1}))
        self.assertContains(response, f'href="{reverse("home")}"')
        self.assertContains(response, f'href="{reverse("board_topics", kwargs={"board_id": 1})}"')

    def test_csrf(self) -> None:
        response = self.client.get(reverse("new_topic", kwargs={"board_id": 1}))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_new_topic_valid_post_data(self) -> None:
        response = self.client.post(
            reverse("new_topic", kwargs={"board_id": 1}),
            data={"subject": "Test title", "message": "Lorem ipsum dolor sit amet"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self) -> None:
        response = self.client.post(
            reverse("new_topic", kwargs={"board_id": 1}),
            data={},
        )
        self.assertEqual(response.status_code, 200)
        form = response.context.get("form")
        self.assertIsInstance(form, NewTopicForm)
        self.assertTrue(bool(form.errors))  # type: ignore[union-attr]  # ty:ignore[unresolved-attribute]

    def test_new_topic_invalid_post_data_empty_fields(self) -> None:
        response = self.client.post(
            reverse("new_topic", kwargs={"board_id": 1}),
            data={"subject": "", "message": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self) -> None:
        response = self.client.get(reverse("new_topic", kwargs={"board_id": 1}))
        form = response.context.get("form")
        self.assertIsInstance(form, NewTopicForm)


class TestNewTopicAnonymousUser(TestCase):
    def test_redirection(self) -> None:
        Board.objects.create(name="Django", description="Django board.")
        url = reverse("new_topic", kwargs={"board_id": 1})
        response = self.client.get(url)

        self.assertRedirects(response, f"{reverse('login')}?next={url}")
