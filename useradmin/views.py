from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category
from django.db.models import Sum
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
    products =  Product.objects.all()
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
        form = AddProductForm()
        return render(request, "useradmin/add-product.html", {"form": form})

