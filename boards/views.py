from typing import TYPE_CHECKING

from django.shortcuts import render

from boards.models import Board

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """Home view."""
    boards = Board.objects.all()
    return render(request, "home.html", {"boards": boards})
