from core.models import Category, Address

def default(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        return {
            'categories': categories
        } 
    try:
        address = Address.objects.get(user=request.user)
        return {
        'categories': categories,
        'address': address,
    }
    except Address.DoesNotExist:
        return {
            'categories': categories
        } 
    