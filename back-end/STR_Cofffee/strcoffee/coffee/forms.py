from django.forms import ModelForm
from .models import Product, Remarkable, Purchase

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class RemarkableForm(ModelForm):
    class Meta:
        model = Remarkable
        fields = ['body']

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['quantity']