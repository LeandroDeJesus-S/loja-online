from django import forms

from .models import ProductVariation


class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        exclude = ()
        widgets = {
            'base_color': forms.widgets.Input({'type': 'color'}),
        }
