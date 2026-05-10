from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from boards.forms import NewTopicForm, PostForm
from boards.models import Board, Post, Topic

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


@login_required
def new_topic(request: HttpRequest, board_id: int) -> HttpResponse:
    """New topics view."""
    board = get_object_or_404(Board, id=board_id)

    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic: Topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=request.user,
            )
            return redirect("topic_posts", board_id=board.pk, topic_id=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, "new_topic.html", {"board": board, "form": form})


def topic_posts(request: HttpRequest, board_id: int, topic_id: int) -> HttpResponse:
    """Topic posts view."""
    topic = get_object_or_404(Topic, id=topic_id, board_id=board_id)
    return render(request, "topic_posts.html", {"topic": topic})


@login_required
def reply_topic(request: HttpRequest, board_id: int, topic_id: int) -> HttpResponse:
    """Reply topic view."""
    topic = get_object_or_404(Topic, id=topic_id, board_id=board_id)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect("topic_posts", board_id=board_id, topic_id=topic_id)
    else:
        form = PostForm()

    return render(request, "reply_topic.html", {"topic": topic, "form": form})
