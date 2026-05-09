from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404, render

from boards.models import Board

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """Home view."""
    boards = Board.objects.all()
    return render(request, "home.html", {"boards": boards})


def board_topics(request: HttpRequest, board_id: int) -> HttpResponse:
    """Board topics view."""
    board = get_object_or_404(Board, id=board_id)
    return render(request, "topics.html", {"board": board})
