from django.db import models

# Create your models here.
class UserTb(models.Model):
    user_no = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20, blank=True, null=True)
    pw = models.CharField(max_length=20, blank=True, null=True)
    nm = models.CharField(max_length=20, blank=True, null=True)
    tel = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_tb'


class LoginTb(models.Model):
    user_id = models.CharField(max_length=20, blank=True, null=True)
    pw = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login_tb'


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=20, blank=True, null=True)
    food_kcal = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

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

class ImageTb(models.Model):
    img_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    date_time = models.DateField()
    img = models.ImageField(upload_to="images/")

    class Meta:
        managed = False
        db_table = 'image_tb'
