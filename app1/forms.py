from django import forms
from .models import *


class shopsignupform(forms.ModelForm):
    class Meta:
        model = shopsignup
        exclude = ['permission'] 

class shop_detailsform(forms.ModelForm):
    class Meta:
        model = shop_details
        exclude = ['my_shop'] 

class shopcrededit(forms.ModelForm):
    class Meta:
        model = shopsignup
        fields = ["shopname", "shop_pic", "shop_license"]
