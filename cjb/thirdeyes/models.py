from django.db import models

# Create your models here.
class UserTb(models.Model):
    user_no = models.AutoField(primary_key=True)
    nm = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    pw = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_tb'

class LoginTb(models.Model):
    user_no = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, blank=True, null=True)
    pw = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login_tb'



class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=20, blank=True, null=True)
    food_kcal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'food'

class UserInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    gender = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    activity = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'



class UserFood(models.Model):
    user_no = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20, blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    meal_type = models.IntegerField(blank=True, null=True)
    food_name = models.CharField(max_length=20, blank=True, null=True)
    food_kcal = models.IntegerField(blank=True, null=True)
    food_cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_food'


class Thirdeyes(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class FoodImage(models.Model):
    user_no = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20, blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    meal_type = models.IntegerField(blank=True, null=True)
    img = models.ImageField(upload_to="images/")

    class Meta:
        managed = False
        db_table = 'food_image'

class UserActivity(models.Model):
    user_no = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20, blank=True, null=True)
    dt = models.DateField(blank=True, null=True)
    act_name = models.CharField(max_length=20, blank=True, null=True)
    act_met = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    act_time = models.IntegerField(blank=True, null=True)
    act_kcal = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_activity'