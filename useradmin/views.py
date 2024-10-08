from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category, CartOrderItem, ProductReview
from userauths.models import Profile
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from userauths.models import User
from useradmin.forms import AddProductForm
from useradmin.decorators import admin_required

import datetime

# Create your views here.

@admin_required
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

@admin_required
def products(request):
    products =  Product.objects.all().order_by("-date")
    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
    }
    
    return render(request, "useradmin/products.html", context)

@admin_required
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


@admin_required
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

@admin_required
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:products")  


@admin_required
def orders(request):
    orders = CartOrder.objects.all().order_by("-order_date")
    context = {
        "orders": orders
    }
    
    return render(request, "useradmin/orders.html", context)

@admin_required
def order_detail(request, oid):
    order = get_object_or_404(CartOrder, oid=oid)
    items = order.items.all()

    context = {
        "order": order,
        "items": items,
    }
    return render(request, "useradmin/order-detail.html", context)


@admin_required
def update_order_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == "POST":
        status = request.POST.get("status")
        order.product_status = status
        order.save()
        messages.success(request, f"Order status changed to {status}")
    return redirect("useradmin:order-detail", order.oid)

@admin_required
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


@admin_required
def reviews(request):
    reviews = ProductReview.objects.all().order_by("-date")
    context = {
        "reviews": reviews,
    }

    return render(request, "useradmin/reviews.html", context)

@admin_required
def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        country = request.POST.get("country")

        if image != None:
            profile.image = image
        profile.full_name = full_name
        profile.email = email
        profile.phone = phone
        profile.address = address
        profile.country = country
        profile.save()
        messages.success(request, "Profile updated successfully")
        return redirect("useradmin:settings")
    context = {
        "profile": profile,
    }
    return render(request, "useradmin/settings.html", context)

@admin_required
def change_password(request):
    user = request.user
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if check_password(old_password, user.password):
            if confirm_password != new_password:
                messages.warning(request, "Passwords do not match")
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Passwords changed successfully")
                return redirect("useradmin:change-password")
        else:
            messages.warning(request, "Old password is incorrect")
            return redirect("useradmin:change-password")
    return render(request, "useradmin/change-password.html")