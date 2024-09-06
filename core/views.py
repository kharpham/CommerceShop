from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Avg
from django.template.loader import render_to_string
from core.models import Product, Category, Vendor, CartOrder, CartOrderItem, WishList, ProductImage, ProductReview, Address
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from core.forms import ProductReviewForm
import math





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

@login_required(login_url="userauths:sign-in")
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

    products = Product.objects.filter(product_status="published").order_by("-id")
    products = products.filter(price__gte=min_price).filter(price__lte=math.ceil(float(max_price)))

    if len(categories) > 0:
        products = products.filter(category__cid__in=categories).distinct()
    if len(vendors) > 0:
        products = products.filter(vendor__vid__in=vendors).distinct()

    data = render_to_string("core/async/product-list.html", {
        "products": products,
    })
    return JsonResponse({"data": data, "product_count": len(products)})
    

