from django.test import TestCase
from django.urls import reverse

from boards.models import Board


class TestBoardTopics(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name="Django", description="Django board.")

    def test_board_topics_views_success_status_code(self) -> None:
        response = self.client.get(reverse("board_topics", kwargs={"board_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self) -> None:
        response = self.client.get(reverse("board_topics", kwargs={"board_id": 2}))
        self.assertEqual(response.status_code, 404)

    def test_board_topics_view_contains_navigation_links(self) -> None:
        response = self.client.get(reverse("board_topics", kwargs={"board_id": 1}))
        self.assertContains(response, f'href="{reverse("home")}"')
        self.assertContains(response, f'href="{reverse("new_topic", kwargs={"board_id": 1})}"')
