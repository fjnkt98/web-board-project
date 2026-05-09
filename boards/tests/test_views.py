from django.test import TestCase
from django.urls import reverse

from boards.models import Board


class TestHome(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name="Django", description="Django board.")

    def test_home(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_contains_link_to_topics_page(self) -> None:
        response = self.client.get(reverse("home"))
        self.assertContains(response, f'href="{reverse("board-topics", kwargs={"board_id": 1})}"')


class TestBoard(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name="Django", description="Django board.")

    def test_board_topics_views_success_status_code(self) -> None:
        response = self.client.get(reverse("board-topics", kwargs={"board_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self) -> None:
        response = self.client.get(reverse("board-topics", kwargs={"board_id": 2}))
        self.assertEqual(response.status_code, 404)

    def test_board_topics_view_contains_link_back_to_homepage(self) -> None:
        response = self.client.get(reverse("board-topics", kwargs={"board_id": 1}))
        self.assertContains(response, f'href="{reverse("home")}"')
