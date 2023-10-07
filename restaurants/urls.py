from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:restaurant_id>/details/", views.details, name="details"),
    path("<int:restaurant_id>/grades/", views.grades, name='grades')
]