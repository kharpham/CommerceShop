from django.urls import path, include
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

    # Search
    path("search/", views.search_view, name="search"),

    # Filter
    path("filtered-products/", views.filter_product, name="filter"),

    # Add product to cart
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),

    # Cart page
    path("cart/", views.cart_view, name="cart"),

    # Remove product from cart
    path("remove-from-cart/", views.remove_from_cart, name="remove-from-cart"),

    # Update product from cart
    path("update-cart/", views.update_cart, name="update-cart"),

    # Checkout
    path("save-checkout-info/", views.save_checkout_info, name="save-checkout-info"),
    path("checkout/<str:oid>/", views.checkout, name="checkout"),

    # Paypal payment
    path("paypal/", include("paypal.standard.ipn.urls")),
    
    # Payment successful
    path("payment-completed/", views.payment_completed_view, name="payment-completed"),

    # Payment failed
    path("payment-failed/", views.payment_failed_view, name="payment-failed"),

    # Dashboard URL
    path("dashboard/", views.customer_dashboard, name="dashboard"),

    # Order detail
    path("dashboard/orders/<int:id>", views.order_detail, name="order-detail"),

    # Make address default
    path("default-address/", views.make_address_default, name="make-address-default"),

    # Wishlist page
    path("wishlist/", views.wishlist_view, name="wishlist"),

    # Add product to wishlist
    path("add-to-wishlist/", views.add_to_wishlist, name="add-to-wishlist"),

    # Remove product from wishlist
    path("remove-from-wishlist/", views.remove_from_withlist, name="remove-from-withlist"),

    # Contact page
    path("contact/", views.contact, name="contact"),

    # Contact with ajax
    path("contact-ajax/", views.contact_ajax, name="contact-ajax"),
]
