from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category, CartOrderItem, ProductReview
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from userauths.models import User
from useradmin.forms import AddProductForm


import datetime

# Create your views here.
def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    orders = CartOrder.objects.all().order_by("-order_date")
    order_count = orders.count()
    products = Product.objects.all()
    categories = Category.objects.all()
    customers = User.objects.all().order_by("-id")
    
    this_month = datetime.datetime.now().month 

    monthly_revenue = (CartOrder.objects.filter(order_date__month=this_month)).aggregate(price=Sum("price"))

    context = {
        "orders": orders,
        "order_count": order_count,
        "revenue": revenue["price"],
        "products": products,
        "categories": categories,
        "customers": customers,
        "monthly_revenue": monthly_revenue,
    }

    return render(request, "useradmin/dashboard.html", context)

def products(request):
    products =  Product.objects.all().order_by("-date")
    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
    }
    
    return render(request, "useradmin/products.html", context)

def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form  = form.save(commit=False)
            new_form.user =  request.user
            new_form.save()
            # Save many to many fields
            form.save_m2m()
            return redirect("useradmin:dashboard")
        else:
            return render(request, "useradmin/add-product.html", {"form": form})
    else:
        form = AddProductForm()
        return render(request, "useradmin/add-product.html", {"form": form})


def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form  = form.save(commit=False)
            new_form.user =  request.user
            new_form.save()
            # Save many to many fields
            form.save_m2m()
            return redirect("useradmin:edit-product", product.pid)
        else:
            return render(request, "useradmin/add-product.html", {"form": form, "product": product})
    else:
        form = AddProductForm(instance=product)
        return render(request, "useradmin/edit-product.html", {"form": form, "product": product})

def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:products")  

def orders(request):
    orders = CartOrder.objects.all().order_by("-order_date")
    context = {
        "orders": orders
    }
    
    return render(request, "useradmin/orders.html", context)

def order_detail(request, oid):
    order = get_object_or_404(CartOrder, oid=oid)
    items = order.items.all()

    context = {
        "order": order,
        "items": items,
    }
    return render(request, "useradmin/order-detail.html", context)

def update_order_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == "POST":
        status = request.POST.get("status")
        order.product_status = status
        order.save()
        messages.success(request, f"Order status changed to {status}")
    return redirect("useradmin:order-detail", order.oid)

def shop_page(request):
    products = Product.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_sales = CartOrderItem.objects.aggregate(quantity=Sum("quantity"))

    context = {
        "products": products,
        "revenue": revenue,
        "total_sales": total_sales,
    }
    return render(request, "useradmin/shop-page.html", context)


def reviews(request):
    reviews = ProductReview.objects.all().order_by("-date")
    context = {
        "reviews": reviews,
    }

    return render(request, "useradmin/reviews.html", context)
