from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, UpdateView

from boards.forms import NewTopicForm, PostForm
from boards.models import Board, Post, Topic

if TYPE_CHECKING:
    from django.forms import ModelForm
    from django.http import HttpRequest, HttpResponse


class BoardListView(ListView):
    model = Board
    context_object_name = "boards"
    template_name = "home.html"


class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"
    template_name = "topics.html"
    paginate_by = 20

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        kwargs["board"] = self.board
        return super().get_context_data(**kwargs)  # ty:ignore[invalid-argument-type]

    def get_queryset(self) -> QuerySet:
        self.board = get_object_or_404(Board, pk=self.kwargs.get("board_id"))
        return self.board.topics.order_by("-last_updated").annotate(replies=Count("posts") - 1)  # ty:ignore[unresolved-attribute]


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
    topic.views += 1
    topic.save()
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


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ("message",)
    template_name = "edit_post.html"
    pk_url_kwarg = "post_id"
    context_object_name = "post"

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form: ModelForm) -> HttpResponse:
        post: Post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect("topic_posts", board_id=post.topic.board.pk, topic_id=post.topic.pk)
