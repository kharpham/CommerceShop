from django.shortcuts import render
from django.http import HttpResponse, Http404
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

def product_list_view_with_category(request, cid):
    try:
        category = Category.objects.get(cid=cid)
        products = Product.objects.filter(product_status="published", category=category)
        return render(request, "core/category-product-list.html", {
            "category": category,
            "products": products,
        })
    except Category.DoesNotExist:
        raise Http404("Category not found.")
        
def vendor_list_view(request):
    vendors = Vendor.objects.all()
    return render(request, "core/vendor-list.html", {"vendors": vendors})

def vendor_detail_view(request, vid):
    try:
        vendor = Vendor.objects.get(vid=vid)
        products = Product.objects.filter(vendor=vendor, product_status="published")
        return render(request, "core/vendor-detail.html", {
            "vendor": vendor,
            "products": products,
            })
    except Vendor.DoesNotExist:
        raise Http404("Vendor not found.")