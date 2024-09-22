from core.models import Product
from django import forms 

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter product title", "class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Product Description", "class":"form-control"}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': "Sale Price", "class":"form-control"}))
    old_price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': "Old Price", "class":"form-control"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Type of product e.g organic cream", "class":"form-control"}))
    stock = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "How many are in stock?", "class":"form-control"}))
    life = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "How long would this product live?", "class":"form-control"}))
    mfg = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'placeholder': "e.g: 24/01/21", "class":"form-control"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Tags", "class":"form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))

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
