from django.urls import path
from . import views

app_name = "durians"

urlpatterns = [
    path("", views.index, name="index")
]
