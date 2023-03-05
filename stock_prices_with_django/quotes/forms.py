from django import forms
from .models import Stock


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        # fields = '__all__'
        fields = ['name']
    # todo:next time complete input from here and change html form
