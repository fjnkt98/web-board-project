from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    def get_posts_count(self) -> int:
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self) -> Post | None:
        return Post.objects.filter(topic__board=self).order_by("-created_at").first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, related_name="topics", on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name="topics", on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="+", null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.message[:30]
