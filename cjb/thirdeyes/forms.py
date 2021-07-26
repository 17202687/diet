from django import forms
from django.forms import fields
from .models import *
 
class MyForm(forms.ModelForm):
  class Meta:
    model = UserTb
    fields = ["user_no","id","pw","nm","tel","email"]

  
class FoodForm(forms.ModelForm):
  class Meta:
    model = Food
    fields = ["food_id", "food_name","food_kcal"]

class LoginForm(forms.ModelForm):
  class Meta:
    model = LoginTb
    fields = ["user_id","pw"]

class UserInfoForm(forms.ModelForm):
  class Meta:
    model = UserInfo
    fields = ["user_id", "gender", "age", "height", "weight", "activity"]

class ImageForm(forms.Form):
  name=forms.CharField()
  image_field=forms.ImageField()