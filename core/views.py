from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Avg, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from core.models import Coupon, Product, Category, Vendor, CartOrder, CartOrderItem, WishList, ProductImage, ProductReview, Address
from userauths.models import ContactUs, Profile
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from core.forms import ProductReviewForm
import math
import stripe

import calendar
from django.db.models.functions import ExtractMonth



# Create your views here.
def index(request):
    products = Product.objects.filter(featured=True, product_status="published")
    return render(request, 'core/index.html', {
        "products": products, 
    })
    

def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by("-id")
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

# @login_required(login_url="userauths:sign-in")
def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    
    # Get all reviews of the product
    reviews = product.reviews.all().order_by("-date")

    #Get average rating of the product
    average_rating = reviews.aggregate(rating=Avg('rating'))

    p_image = product.product_images.all()
    vendor = product.vendor

    # Product review form
    review_form = ProductReviewForm()

    is_authenticated = request.user.is_authenticated
    allow_to_add_review = True
    if is_authenticated:
        user_review_count = reviews.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            allow_to_add_review = False
    return render(request, "core/product-detail.html", {
        "product": product,
        "vendor": vendor,
        "products": products,
        "p_image": p_image,
        "reviews": reviews,
        "average_rating": average_rating,
        "review_form": review_form,
        "is_logged_in": is_authenticated,
        "allow_to_add_review": allow_to_add_review,
    })

def tag_list(request, tag_slug=None):
    products = Product.filter(product_status="published").order_by("-id")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    return render(request, "core/tag.html", {
        "products": products,
        "tag": tag,
    })

@login_required()
def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating']
    )
    
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }
    average_rating = product.reviews.all().aggregate(rating=Avg("rating"))

    return JsonResponse({
        'bool': True,
        'context': context,
        'average_rating': average_rating,
        'date': review.date.strftime('%d %B, %Y'),
    })

def search_view(request):
    query = request.GET["q"]

    products = Product.objects.filter(title__icontains=query).order_by("-date") 
    context = {
        "products": products,
        "query": query,
    }

    return render(request, "core/search.html", context)

def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id", "date")
    products = products.filter(price__gte=min_price).filter(price__lte=math.ceil(float(max_price)))

    if len(categories) > 0:
        products = products.filter(category__cid__in=categories).distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__vid__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {
        "products": products,
    })
    return JsonResponse({"data": data, "product_count": len(products)})

def add_to_cart(request):
    cart_product = {}
    title = request.GET["title"]
    pid = request.GET["pid"]
    quantity = int(request.GET["quantity"])
    price = float(request.GET["price"])
    image = request.GET["image"]

    cart_product[pid] = {
        'title': title,
        'quantity': quantity,
        'price': price,
        'image': image,
        'pid': pid,
    }
    
    if "cart_data_object" in request.session:
        cart_data = request.session["cart_data_object"]
        cart_data[pid] = cart_product[pid]
        # Save the cart data back to the session
        request.session["cart_data_object"] = cart_data
    else:
        request.session["cart_data_object"] = cart_product
    return JsonResponse({"data": request.session["cart_data_object"], "total_cart_items": len(request.session["cart_data_object"])})


def cart_view(request):
    cart_total_amount = 0
    product_amount = 0
    cart_data = ""
    if "cart_data_object" in request.session:
        for pid, item in request.session["cart_data_object"].items():
            cart_total_amount += item['quantity'] * item['price']
        product_amount = len(request.session["cart_data_object"])
        cart_data = reversed(request.session["cart_data_object"].values())
    context = {
            'cart_total_amount': cart_total_amount,
            'cart_data': cart_data,
            'product_amount': product_amount,
    }
    return render(request, "core/cart.html", context)

def remove_from_cart(request):
    pid = request.GET["pid"]
    cart_data = request.session["cart_data_object"]
    if pid in cart_data:
        del cart_data[pid]
        product_amount = len(cart_data)
        cart_total_amount = 0
        for product in cart_data.values():
            cart_total_amount += product['price'] * product['quantity']
        request.session["cart_data_object"] = cart_data
        # Explicitly mark the session as modified
        request.session.modified = True
        data = {
            "product_amount": product_amount,
            "cart_total_amount": cart_total_amount,
        }
        return JsonResponse({"data": data})
    return JsonResponse({"data": cart_data, "message": "Product PID not found in cart."}, status=404)

def update_cart(request):
    pid = request.GET["pid"]
    quantity = request.GET["quantity"]
    cart_data = request.session["cart_data_object"]
    product_subtotal = cart_data[pid]["quantity"] * cart_data[pid]["price"]
    cart_total_amount = 0
    if pid in cart_data:
        cart_data[pid]["quantity"] = int(quantity)
        product_subtotal = int(quantity) * cart_data[pid]["price"]    
    for product in cart_data.values():
        cart_total_amount += product['quantity'] * product['price']
    request.session["cart_data_object"] = cart_data
    request.session.modified = True
    return JsonResponse({"data": {"product_subtotal": product_subtotal, "cart_total_amount": cart_total_amount}})

def save_checkout_info(request):
    cart_total_amount = 0   

    if request.method == "POST":
        full_name = request.POST["full_name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        address = request.POST["address"]
        city = request.POST["city"]
        state  = request.POST["state"]
        country = request.POST["country"]
        # request.session["mobile"] = mobile
        # request.session["email"] = email
        request.session["address"] = address
        # request.session["full_name"] = full_name
        request.session["city"] = city
        request.session["state"] = state
        request.session["country"] = country
        if "cart_data_object" in request.session and len(request.session["cart_data_object"]) > 0:
            cart_data = request.session["cart_data_object"]
            # Get the cart total amount
            for product in cart_data.values():
                cart_total_amount += product["quantity"] * product["price"]
            # Create new order
            order = CartOrder.objects.create(
                user=request.user,
                price=cart_total_amount,
                full_name=full_name,
                email=email,
                address=address,
                city=city,
                state=state,
                phone=mobile,
                country=country,
            )
            # del request.session["email"]
            # del request.session["mobile"]
            # del request.session["address"]
            # del request.session["full_name"]
            # del request.session["city"]
            # del request.session["state"]
            # del request.session["country"]

            for product in cart_data.values():
                cart_order_item = CartOrderItem.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id),
                    item=product["title"],
                    image=product["image"],
                    quantity=product['quantity'],
                    price=product['price'],
                    total=product['price'] * product['quantity'],
                )
            return redirect("core:checkout", order.oid)
        return JsonResponse({"message": "Your cart is empty"}, status=400)

def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = order.items.all()
    context = {
        "order": order,
        "order_items": order_items,
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
    }
    # Handling coupon submission
    if request.method == "POST":
        code = request.POST.get("code")   
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon: 
            if coupon in order.coupons.all():
                messages.warning(request, "Coupon already activated.")
                return redirect("core:checkout", order.oid)
            else:
                discount = order.price * coupon.discount / 100
                order.coupons.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()
                messages.success(request, "Coupon activated successfully.")
                return redirect("core:checkout", order.oid)
        else: 
            messages.warning(request, "Coupon does not exist.")
            return redirect("core:checkout", order.oid)

    
    return render(request, "core/checkout.html", context)

@csrf_exempt
def create_checkout_session(request, oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email= order.email,
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data': {
                    'currency': "USD",
                    "product_data": {
                        'name': order.full_name 
                    },
                    "unit_amount": int(order.price * 100)
                }, 
                'quantity': 1
            },
        ],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse("core:payment-completed", args=[order.oid])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse("core:payment-failed")),
    )
    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    return JsonResponse({"sessionId": checkout_session.id})



def payment_completed_view(request, oid):
    cart_total_amount = 0
    current_date = datetime.now()
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()
    if "cart_data_object" in request.session and len(request.session['cart_data_object']) > 0:
        cart_data = request.session["cart_data_object"]
        for product in cart_data.values():
            cart_total_amount += product['price'] * product['quantity']
        # Clear the session cart data object
        # del request.session["cart_data_object"]
        # request.session.modified = True
        del request.session['cart_data_object']
        # Optionally, save the session to apply the changes
        request.session.modified = True
        return render(request, "core/payment-success.html", {
            'cart_total_amount': cart_total_amount,
            'product_amount': len(cart_data),
            'cart_data': cart_data.values(),
            'current_date': current_date,
            'oid': oid,
        })
    else:
        for item in order.items.all():
            cart_total_amount += item.price * item.quantity
        return render(request, "core/payment-success.html", {
            'cart_total_amount': cart_total_amount,
            'product_amount': order.items.count(),
            'cart_data': order.items.all(),
            'current_date': current_date,
            'oid': oid,
        })


def payment_failed_view(request):
    return render(request, "core/payment-failed.html")

@login_required()
def customer_dashboard(request):
    orders = request.user.cart_orders.all().order_by("-order_date")
    addresses =  Address.objects.filter(user=request.user)
    profile = Profile.objects.filter(user=request.user)

    order_distribution = request.user.cart_orders.all().annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    months = []
    total_orders = []

    for order in order_distribution:
        months.append(calendar.month_name[order['month']])
        total_orders.append(order["count"])

    if request.method == "POST":
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile
        )
        return redirect("core:dashboard")
    context = {
        "orders": orders,
        "addresses": addresses,
        "order_distribution": order_distribution,
        "months": months,
        "total_orders": total_orders,
        "profile": profile[0], 
    }
    return render(request, 'core/dashboard.html', context)

@login_required()
def order_detail(request, id):
    try: 
        order = CartOrder.objects.get(user=request.user, id=id)
        order_items = order.items.all()

        context = {
            "order_items": order_items,
            "order": order,
        }
        return render(request, 'core/order-detail.html', context)
    except CartOrder.DoesNotExist:
        raise Http404("Order does not exist.")

def make_address_default(request):
        address_id = request.GET["address_id"]
        try:
            address =Address.objects.get(id=address_id)
            try:
                undefault_address = Address.objects.get(status=True, user=request.user)
                undefault_address.status = False
                undefault_address.save()
                address.status = True
                address.save()
                return JsonResponse({"data": {"undefault": undefault_address.id}})
            except Address.DoesNotExist:
                address.status = True
                address.save()
                return JsonResponse({"data": {"undefault": "None"}})
        except Address.DoesNotExist:
            raise Http404({"message": "Address does not exist."}, status=404)
 
@login_required
def wishlist_view(request):
    wishlist = WishList.objects.filter(user=request.user)
    context = {
        "wishlist": wishlist,
    }
    return render(request, "core/wishlist.html", context)
    

@login_required()
def add_to_wishlist(request):
    product_pid = request.GET["product_pid"]
    try:
        product = Product.objects.get(pid=product_pid)
        existing_wishlist = WishList.objects.filter(product=product, user=request.user)
        if len(existing_wishlist) > 0:
            return JsonResponse({"message": "Product is already in the wishlist"}, status=400)
        wishlist = WishList.objects.create(product=product, user=request.user)
        wishlist_amount = len(WishList.objects.filter(user=request.user))
        return JsonResponse({"message": "Product added to wishlist successfully...", "wishlist_amount": wishlist_amount})
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product does not exist"}, status=404)
    
@login_required()
def remove_from_withlist(request):
    product_pid = request.GET["product_pid"]
    try:
        product = Product.objects.get(pid=product_pid)
        removed_product = get_object_or_404(WishList, product=product, user=request.user)
        removed_product.delete()
        wishlist_amount = len(WishList.objects.filter(user=request.user))
        return JsonResponse({"message": "Product removed from wishlist successfully...", "wishlist_amount": wishlist_amount})
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product does not exist"}, status=404)

def contact(request):
    return render(request, "core/contact.html")

@login_required()
def contact_ajax(request):
    full_name = request.POST["full_name"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    subject = request.POST["subject"]
    message = request.POST["message"]
    
    contact_form = ContactUs.objects.create(full_name=full_name, email=email, phone=phone, subject=subject, message=message)
    context = {
        "bool": True,
        "message": "Contact form sent to the server successfully...",
    }
    return JsonResponse({"data": context})



