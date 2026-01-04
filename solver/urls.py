from django.urls import path

from . import views

app_name = "solver"
urlpatterns = [
    # ex: /solver/
    path("", views.index, name="index"),
]