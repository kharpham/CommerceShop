from django.urls import path
from . import views

app_name = "useradmin"

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
