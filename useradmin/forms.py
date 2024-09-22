from core.models import Product
from django import forms 

class AddProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'type',
            'stock',
            'life',
            'mfg',
            'tags',
            'digital',
            'category',
        ]
