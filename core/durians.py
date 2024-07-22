from django.urls import path
from . import views

app_name = "durians"

urlpatterns = [
    path("durians/", views.index)
]
