from django import forms
from .models import QuickAdd, Product

"""class QuickProductForm(forms.ModelForm):
    class Meta:
        model = QuickProduct
        fields = '__all__'"""


class QuickAddForm(forms.ModelForm):
    class Meta:
        model = QuickAdd
        fields = ('name', 'stock', 'maaliyet', 'satisFiyati', 'kdvOrani')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'stock'
            }),
            'maaliyet': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'maaliyet'
            }),
            'satisFiyati': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'satisFiyati'
            }),
            'kdvOrani': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'kdvOrani'
            })
        }
        # CURRENCY_CHOICES = [
        #     ('USD', 'Dolar'),
        #     ('EUR', 'Euro'),
        #     ('TRY', 'Türk Lirası'),
        #     # Diğer para birimleri buraya eklenebilir
        # ]
        #
        # category = forms.ModelChoiceField(queryset=Category.objects.all())
        # currency = forms.ChoiceField(choices=CURRENCY_CHOICES)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sortno']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'sortno': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'sortno'
            })
        }