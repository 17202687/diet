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

class mealForm(forms.ModelForm):
  class Meta:
    model = UserFood
    fields = ["user_no", "id", "dt", "meal_type", "food_name", "food_kcal", "food_cnt"]


class foodImageForm(forms.Form):
  id=forms.CharField()
  dt=forms.DateField()
  meal_type=forms.IntegerField()
  image_field=forms.ImageField()
