from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from core.models import Product, Category, Vendor, CartOrder, CartOrderItem, WishList, ProductImage, ProductReview, Address
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from core.forms import ProductReviewForm
import math
from paypal.standard.forms import PayPalPaymentsForm



# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
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

@login_required()
def checkout(request):
    cart_total_amount = 0
    # Check if cart_data_object exists in the session and there's more than 1 product in the cart
    if "cart_data_object" in request.session and len(request.session["cart_data_object"]) > 0:
        cart_data = request.session["cart_data_object"]
        # Get the cart total amount
        for product in cart_data.values():
            cart_total_amount += product["quantity"] * product["price"]
        # Create new order
        order = CartOrder.objects.create(
            user=request.user,
            price=cart_total_amount,
        )

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



        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": f"{cart_total_amount:.2f}",
            "item_name": "Order-Item-No-" + str(order.id),
            "invoice": "INVOICE-NO-" + str(order.id),
            "notify_url": request.build_absolute_uri(reverse('core:paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('core:payment-completed')),
            "cancel_url": request.build_absolute_uri(reverse('core:payment-failed')),
            "currency_code": "USD",
        }
        form = PayPalPaymentsForm(initial=paypal_dict)

        address = ""
        try:
            address = request.user.address.get(status=True)
        except Address.DoesNotExist:
            address = ""
        return render(request, "core/checkout.html", {
            "cart_data": cart_data.values(),
            "cart_total_amount": cart_total_amount,
            "product_amount": len(cart_data),
            "form": form,
            "address": address,
        })
    
    
    messages.add_message(request, messages.WARNING, 'Your cart is empty...')
    return redirect('core:index')

@login_required()
def payment_completed_view(request):
    cart_total_amount = 0
    current_date = datetime.now()
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
        })
    return redirect("core:index")

@login_required()
def payment_failed_view(request):
    return render(request, "core/payment-failed.html")

@login_required()
def customer_dashboard(request):
    orders = request.user.cart_orders.all().order_by("-order_date")
    addresses =  Address.objects.filter(user=request.user)

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
    
    