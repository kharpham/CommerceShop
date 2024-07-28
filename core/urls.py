from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    # Homepage
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),

    # Categories
    path("categories/",views.category_list_view, name="category-list"),
    path("categories/<str:cid>", views.product_list_view_with_category, name="product-list-with-category"),

    # Vendor
    path("vendors/", views.vendor_list_view, name="vendor-list"),
    path("vendors/<str:vid>", views.vendor_detail_view, name="vendor-detail"),
]
