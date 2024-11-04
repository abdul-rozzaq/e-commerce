from django import forms
from .models import Review, CartItem


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        exclude = ["product"]


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['count', 'color', 'size']