from django.shortcuts import render, redirect
from core.models import CartOrder, Product, Category
from django.db.models import Sum
from userauths.models import User

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