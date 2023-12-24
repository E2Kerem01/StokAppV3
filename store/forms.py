from django import forms
from .models import QuickAdd, Product, Category

"""class QuickProductForm(forms.ModelForm):
    class Meta:
        model = QuickProduct
        fields = '__all__'"""


class QuickAddForm(forms.ModelForm):
    class Meta:
        model = QuickAdd
        fields = ('name', 'stock', 'maaliyet', 'satisFiyati', 'kdvOrani', 'currency', 'category')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'id': 'stock'}),
            'maaliyet': forms.NumberInput(attrs={'class': 'form-control', 'id': 'maaliyet'}),
            'satisFiyati': forms.NumberInput(attrs={'class': 'form-control', 'id': 'satisFiyati'}),
            'kdvOrani': forms.NumberInput(attrs={'class': 'form-control', 'id': 'kdvOrani'}),
            'currency': forms.Select(attrs={'class': 'form-control', 'id': 'currency'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
        }

    def __init__(self, *args, **kwargs):
        super(QuickAddForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

        # CURRENCY_CHOICES = [
        #     ('USD', 'Dolar'),
        #     ('EUR', 'Euro'),
        #     ('TRY', 'Türk Lirası'),
        #     # Diğer para birimleri buraya eklenebilir
        # ]
        #
        # category = forms.ModelChoiceField(queryset=Category.objects.all())
        # currency = forms.ChoiceField(choices=CURRENCY_CHOICES)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'description'
            })
        }


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
