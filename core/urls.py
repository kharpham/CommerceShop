from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    # Homepage
    path("", views.index, name="index"),
    path("products/", views.product_list_view, name="product-list"),
    path("products/<str:pid>", views.product_detail_view, name="product-detail"),

    # Categories
    path("categories/",views.category_list_view, name="category-list"),
    path("categories/<str:cid>", views.product_list_view_with_category, name="product-list-with-category"),

    # Vendor
    path("vendors/", views.vendor_list_view, name="vendor-list"),
    path("vendors/<str:vid>", views.vendor_detail_view, name="vendor-detail"),

    # Tag
    path("products/tag/<slug:tag_slug>", views.tag_list, name="product-list-with-tag"),

    # Add Review
    path("ajax-add-review/<str:pid>", views.ajax_add_review, name="ajax-add-review"),
]
