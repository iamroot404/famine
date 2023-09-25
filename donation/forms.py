from django.forms import ModelForm
from .models import Donation, Items, Area
from django import forms


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'mpesa_id']
    
    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ItemsForm(ModelForm):
    class Meta:
        model = Items
        fields = ['item', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class AreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['region', 'county', 'country']
    
    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'