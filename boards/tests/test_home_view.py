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
        self.assertContains(response, f'href="{reverse("board_topics", kwargs={"board_id": 1})}"')
