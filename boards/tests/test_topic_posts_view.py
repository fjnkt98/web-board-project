from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from boards.models import Board, Post, Topic


class TestTopicPosts(TestCase):
    def setUp(self) -> None:
        board = Board.objects.create(name="Django", description="Django board.")
        user = User.objects.create_user("john", "john@example.com", "complexpassword123")
        topic = Topic.objects.create(subject="Hello, world!", board=board, starter=user)

        Post.objects.create(message="Lorem ipsum dolor sit amet", topic=topic, created_by=user)
        self.response = self.client.get(reverse("topic_posts", kwargs={"board_id": board.pk, "topic_id": topic.pk}))

    def test_status_code(self) -> None:
        self.assertEqual(self.response.status_code, 200)
