from django.contrib import admin
from django.urls import path

import boards.views

admin.site.site_header = "Web Board Admin"
admin.site.site_title = "Web Board Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", boards.views.home, name="home"),
    path("boards/<int:board_id>/", boards.views.board_topics, name="board-topics"),
]
