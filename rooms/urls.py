from django.urls import path
from rooms import views

urlpatterns = [
    path("", views.HomeVIew.as_view(), name="home"),
]
