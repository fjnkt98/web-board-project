from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from boards.forms import NewTopicForm
from boards.models import Board, Post

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


def new_topic(request: HttpRequest, board_id: int) -> HttpResponse:
    """New topics view."""
    board = get_object_or_404(Board, id=board_id)
    user = get_object_or_404(User, id=1)

    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=user,
            )
            return redirect("board-topics", board_id=board.pk)
    else:
        form = NewTopicForm()
    return render(request, "new_topic.html", {"board": board, "form": form})
