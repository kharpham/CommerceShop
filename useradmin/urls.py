from django.urls import path
from . import views

app_name = "useradmin"

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    path("products/", views.products, name="products"),

    path('add-product/', views.add_product, name="add-product"),

    path("edit-product/<str:pid>", views.edit_product, name="edit-product"),

    path("delete-product/<str:pid>", views.delete_product, name="delete-product"),
]
