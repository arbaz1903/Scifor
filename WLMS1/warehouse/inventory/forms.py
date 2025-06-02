from django import forms
from .models import Product, Warehouse, Inventory, ProductCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the queryset or ordering if needed
        self.fields['category'].queryset = ProductCategory.objects.all().order_by('name')
        
class ProductForm(forms.ModelForm):
    category_name = forms.CharField(label="Category")

    class Meta:
        model = Product
        fields = ['name', 'description', 'category_name', 'sku']  # exclude 'category'

    def save(self, commit=True):
        instance = super().save(commit=False)
        category_name = self.cleaned_data['category_name']
        category, created = ProductCategory.objects.get_or_create(name=category_name)
        instance.category = category
        
        if commit:
            instance.save()
        return instance
# forms.py
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'weight', 'description', 'category']  # Exclude auto-generated SKU
        widgets = {
            'weight': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False
    # def clean_sku(self):
    #     sku = self.cleaned_data['sku']
    #     if Product.objects.filter(sku=sku).exists():
    #         raise forms.ValidationError("This SKU already exists")
    #     return sku

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
        }

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'warehouse', 'quantity_on_hand', 'quantity_allocated']

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }