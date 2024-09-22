from django.urls import path
from . import views

app_name = "useradmin"

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Product CRUD
    path("products/", views.products, name="products"),

    path('add-product/', views.add_product, name="add-product"),

    path("edit-product/<str:pid>", views.edit_product, name="edit-product"),

    path("delete-product/<str:pid>", views.delete_product, name="delete-product"),

    # Orders

    path("orders/", views.orders, name="orders"),
    
    path("order-detail/<str:oid>", views.order_detail, name="order-detail"),

    path("update-order-status/<str:oid>", views.update_order_status, name="update-order-status"),
]
