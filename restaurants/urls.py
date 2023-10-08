from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:restaurant_id>/details/", views.details, name="details"),
    path("<int:restaurant_id>/grades/", views.grades, name='grades'),
    path("add_restaurant", views.add_restaurant, name='add_restaurant'),
    path("<int:restaurant_id>/update_restaurant/", views.update_restaurant, name='update_restaurant'),
    path("<int:restaurant_id>/delete_restaurant/", views.delete_restaurant, name='delete_restaurant')
]