from core.models import Category, Address, Vendor

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    if not request.user.is_authenticated:
        return {
            'categories': categories,
            'vendors': vendors,
        } 
    try:
        address = Address.objects.get(user=request.user)
        return {
        'categories': categories,
        'address': address,
        'vendors': vendors,
    }
    except Address.DoesNotExist:
        return {
            'categories': categories,
            'vendors': vendors,
        } 
    