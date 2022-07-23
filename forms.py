from logging import PlaceHolder
from django import forms  


class create(forms.Form):  
    title = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'PlaceHolder':'Enter Title'}))
    description = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'PlaceHolder':' Product Description'}))
    category = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'PlaceHolder':'Enter Category'}))
    price = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={'PlaceHolder':'Enter Price'}))
    image = forms.URLField(label='', required=False, widget=forms.URLInput(attrs={'PlaceHolder':'Enter Image URL'}))

class bid(forms.Form):
    amount = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={'PlaceHolder':'Enter Your Bid'}))
    
class close(forms.Form):
    pass

class watchlist(forms.Form):
    pass

class remove_watchlist(forms.Form):
    pass

class comment(forms.Form):
    content = forms.CharField(label='',required=False , widget= forms.Textarea(attrs={"rows":5, "cols":5, 'placeholder':'Enter Comment'}))