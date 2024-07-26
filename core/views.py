from django.shortcuts import render
from django.http import HttpResponse
from core.models import Product, Category, Vendor, CartOrder, CartOrderItem, WishList, ProductImage, ProductReview, Address

# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(featured=True, product_status="published")
    return render(request, 'core/index.html', {
        "products": products, 
    })

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    return render(request, 'core/product-list.html', {
        "products": products, 
    })

def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'core/category-list.html', {"categories": categories})

