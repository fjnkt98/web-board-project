from typing import TYPE_CHECKING

from django.contrib.auth import login
from django.shortcuts import redirect, render

from accounts.forms import SignupForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def signup(request: HttpRequest) -> HttpResponse:
    """Signup view."""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})
