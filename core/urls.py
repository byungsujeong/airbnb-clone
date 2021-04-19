from django.urls import path
from rooms import views

app_name = "core"

urlpatterns = [
    path("", views.HomeVIew.as_view(), name="home"),
]
