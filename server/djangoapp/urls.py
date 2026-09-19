from django.urls import path
from . import views

urlpatterns = [
    path("get_dealers", views.get_dealers),
    path("get_dealers/<str:state>", views.get_dealers_by_state),
    path("dealer/<int:dealer_id>", views.get_dealer_by_id),
    path("review/dealer/<int:dealer_id>", views.get_dealer_reviews),
    path("get_cars", views.get_cars),
    path("get_cars/<str:make>", views.get_car_models),
    path("register", views.register),
    path("login", views.login_user),
    path("logout", views.logout_user),
    path("add_review", views.add_review),
    path("analyze/<str:text>", views.analyze_review),
]
