from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
    path("categories/",views.category_list_view, name="category-list"),
    path("categories/<str:cid>", views.product_list_view_with_category, name="product-list-with-category"),
]
