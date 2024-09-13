from core.models import Category, Address, Vendor, Product, WishList
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    user_wishlist = []
    if request.user.is_authenticated:
        user_wishlist = [item.product.pid for item in WishList.objects.filter(user=request.user)]
    # if not request.user.is_authenticated:
    #     return {
    #         'categories': categories,
    #         'vendors': vendors,
    #     } 
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories': categories,
        'vendors': vendors,
        'address': address,
        'min_max_price': min_max_price,
        'user_wishlist': user_wishlist,
    } 
    