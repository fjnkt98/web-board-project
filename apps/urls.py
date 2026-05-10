from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

import accounts.views
import boards.views

admin.site.site_header = "Web Board Admin"
admin.site.site_title = "Web Board Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", boards.views.home, name="home"),
    path("boards/<int:board_id>/", boards.views.board_topics, name="board-topics"),
    path("boards/<int:board_id>/new/", boards.views.new_topic, name="new-topic"),
    path("accounts/signup/", accounts.views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html",
            email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("accounts/reset/<str:uidb64>/<str:token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
    path("accounts/password_change/", auth_views.PasswordChangeView.as_view(template_name="password_change.html"), name="password_change"),
    path("accounts/password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="password_change_done.html"), name="password_change_done"),
]
