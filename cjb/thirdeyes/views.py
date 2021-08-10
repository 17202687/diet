from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import date
import bcrypt
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ThirdeyesSerializer

# Create your views here.

def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        data=request.POST
        inputId=data['email']
        inputPw=data['pw']
        hashed_pw=bcrypt.hashpw(inputPw.encode('utf-8'),bcrypt.gensalt())
        encoded_pw=hashed_pw.decode('utf-8')
        print(encoded_pw)
        if UserTb.objects.filter(id=data['id']).exists():
            getUser=UserTb.objects.get(id=inputId)
            #if(getUser.pw == inputPw):
            if(bcrypt.checkpw(inputPw.encode('utf-8'),getUser.pw.encode('utf-8'))):
                #로그인 성공
                dt=date.today()
                dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
                request.session['date']=dt2
                request.session['id']=data['email']
                print(request.session['id'])
                return redirect('main/')
            else:
                #비밀번호가 다름
                messages.success(request, '비밀번호가 다릅니다.')
        else:
            #존재하지 않는 아이디
            messages.success(request, '존재하지 않는 아이디입니다.')
    else:
        form=LoginForm()
    return render(request, 'thirdeyes/login.html',{'forms':form})

def main(request):
    requestId=request.session['id']
    dt=date.today()
    dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
    if UserInfo.objects.filter(user_id=requestId).exists():
        getUser=UserInfo.objects.get(user_id=requestId)
        get=UserFood.objects.filter(id=requestId,dt=dt2)
        sum=0
        for a in get:
            sum+=a.food_kcal*a.food_cnt
        print(sum)
        if getUser.gender==1:
            value=((13.7516*getUser.weight)+(5.0033*getUser.height)-(6.7550*getUser.age)+66.4730)*(1+(float(getUser.activity)))
        return render(request, 'thirdeyes/main.html',{'content':value, 'eats':get, 'sum':sum})
    return render(request, 'thirdeyes/main.html') 

def set(request):
    return render(request, 'thirdeyes/set.html')

def signup(request):
    if request.method == "POST":
        data=request.POST
        inputPw=data['pw']
        hashed_pw=bcrypt.hashpw(inputPw.encode('utf-8'),bcrypt.gensalt())
        encoded_pw=hashed_pw.decode('utf-8')
        form = MyForm(request.POST)
        form.pw=encoded_pw
        if form.is_valid():
            data=request.POST
            #id_value=data['id']#form.cleaned_data.get('id')
            if UserTb.objects.filter(id=data['email']).exists():
                context={
                    "result": "이미 존재하는 아이디입니다."
                }
            else:
                UserTb.objects.create(
                    nm=data['nm'],
                    pw=encoded_pw,
                    email=data['email']
                )
                LoginTb.objects.create(
                    user_id=data['email'],
                    pw=encoded_pw
                )
                return redirect('/')
    else:
        form = MyForm()
    return render(request, 'thirdeyes/signup.html', {'form': form})

def user(request):
    requestId=request.session['id']
    print(requestId)
    if UserInfo.objects.filter(user_id=requestId).exists():
        getUser=UserInfo.objects.get(user_id=requestId)
        value={
            'gender':getUser.gender,
            'age':getUser.age,
            'height':getUser.height,
            'weight':getUser.weight,
            'activity':getUser.activity
        }
    else:
        value={
            'gender':0,
            'age':0,
            'height':0,
            'weight':0,
            'activity':0
        }
    if request.method=="POST":
        form = UserInfoForm(request.POST)
        data=request.POST
        if UserInfo.objects.filter(user_id=requestId).exists():
            getUser=UserInfo.objects.get(user_id=requestId)
            getUser.gender=data['gender']
            getUser.age=data['age']
            getUser.height=data['height']
            getUser.weight=data['weight']
            getUser.activity=data['activity']
            getUser.save()
            return redirect('/main/set/')
        else:
            UserInfo.objects.create(
                user_id=requestId,
                gender=data['gender'],
                age=data['age'],
                height=data['height'],
                weight=data['weight'],
                activity=data['activity']
            )
            return redirect('/main/set/')
    else:
        form=LoginForm()
    return render(request, 'thirdeyes/user.html',{'forms':form, 'context':value})

def lunch(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            img=request.FILES["image_field"]
            print(img)
            if(FoodImage.objects.filter(id=request.session['id'],meal_type=2,dt=request.session['date']).exists()):
                obj=FoodImage.objects.get(id=request.session['id'],meal_type=2,dt=request.session['date'])
                obj.img=img
                obj.save()
            else:
                obj=FoodImage.objects.create(
                    id=request.session['id'],
                    meal_type=2,
                    dt=request.session['date'],
                    img=img
                )
                obj.save()
                print(obj)
            return redirect('/main/lunch')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=2,dt=request.session['date'])
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=2).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=2)
        getUrl=getImg.img.url
        print(getUrl)
        return render(request, 'thirdeyes/lunch.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/lunch.html',{'foods':getFood})

def dinner(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            img=request.FILES["image_field"]
            print(img)
            if(FoodImage.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date']).exists()):
                obj=FoodImage.objects.get(id=request.session['id'],meal_type=3,dt=request.session['date'])
                obj.img=img
                obj.save()
            else:
                obj=FoodImage.objects.create(
                    id=request.session['id'],
                    meal_type=3,
                    dt=request.session['date'],
                    img=img
                )
                obj.save()
                print(obj)
            return redirect('/main/dinner')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date'])
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=3,dt=request.session['date'])
        getUrl=getImg.img.url
        print(getUrl)
        return render(request, 'thirdeyes/dinner.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/dinner.html',{'foods':getFood})

def morning(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            img=request.FILES["image_field"]
            print(img)
            if(FoodImage.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date']).exists()):
                obj=FoodImage.objects.get(id=request.session['id'],meal_type=1,dt=request.session['date'])
                obj.img=img
                obj.save()
            else:
                obj=FoodImage.objects.create(
                    id=request.session['id'],
                    meal_type=1,
                    dt=request.session['date'],
                    img=img
                )
                obj.save()
                print(obj)
            return redirect('/main/morning')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date'])
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=1,dt=request.session['date'])
        getUrl=getImg.img.url
        print(getUrl)
        return render(request, 'thirdeyes/morning.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/morning.html',{'foods':getFood})

def snack(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            img=request.FILES["image_field"]
            print(img)
            if(FoodImage.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date']).exists()):
                obj=FoodImage.objects.get(id=request.session['id'],meal_type=4,dt=request.session['date'])
                obj.img=img
                obj.save()
            else:
                obj=FoodImage.objects.create(
                    id=request.session['id'],
                    meal_type=4,
                    dt=request.session['date'],
                    img=img
                )
                obj.save()
                print(obj)
            return redirect('/main/snack')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date'])
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=4,dt=request.session['date'])
        getUrl=getImg.img.url
        print(getUrl)
        return render(request, 'thirdeyes/snack.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/snack.html',{'foods':getFood})

def alarm(request):
    return render(request, 'thirdeyes/alarm.html')

def diary(request):
    return render(request, 'thirdeyes/diary.html')

def malarm(request):
    return render(request, 'thirdeyes/malarm.html')

def lalarm(request):
    return render(request, 'thirdeyes/lalarm.html')

def dalarm(request):
    return render(request, 'thirdeyes/dalarm.html')

def msearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal']),
            food_cnt=1
        )
        return redirect('/main/morning/')
    return render(request, 'thirdeyes/msearch.html', {'foods':getFood, 'id':request.session['id'],'date':request.session['date']})

def lsearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal']),
            food_cnt=1
        )
        return redirect('/main/lunch/')
    return render(request, 'thirdeyes/lsearch.html', {'foods':getFood, 'id':request.session['id'],'date':request.session['date']})

def dsearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal']),
            food_cnt=1
        )
        return redirect('/main/dinner/')
    return render(request, 'thirdeyes/dsearch.html', {'foods':getFood, 'id':request.session['id'],'date':request.session['date']})

def ssearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal']),
            food_cnt=1
        )
        return redirect('/main/snack/')
    return render(request, 'thirdeyes/ssearch.html', {'foods':getFood, 'id':request.session['id'],'date':request.session['date']})

def mfoodedit(request):
    if request.method=="POST":
        data=request.POST
        i=0
        getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=1)
        getFood.delete()
        foodnames=data.getlist('food_name')[0].split(",")
        foodcnt=data.getlist('foodcnt')[0].split(",")
        while i<len(data.getlist('p_price')):
            UserFood.objects.create(
                id=request.session['id'],
                dt=request.session['date'],
                meal_type=1,
                food_name=foodnames[i],
                food_kcal=int(data.getlist('p_price')[i]),
                food_cnt=int(foodcnt[i])
            )
            i+=1
        return redirect("/main/morning/")
    getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=1)
    sum=0
    kcal=[0]
    cnt=0
    amount=0
    for food in getFood:
        sum+=food.food_kcal*food.food_cnt
        kcal.append(food.food_kcal*food.food_cnt)
        cnt+=food.food_cnt
        amount+=1
    return render(request, 'thirdeyes/mfoodedit.html',{'foods':getFood,'sum':sum,'kcal':kcal,'cnt':cnt,'amount':amount})

def lfoodedit(request):
    if request.method=="POST":
        data=request.POST
        i=0
        getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=2)
        getFood.delete()
        foodnames=data.getlist('food_name')[0].split(",")
        foodcnt=data.getlist('foodcnt')[0].split(",")
        while i<len(data.getlist('p_price')):
            UserFood.objects.create(
                id=request.session['id'],
                dt=request.session['date'],
                meal_type=2,
                food_name=foodnames[i],
                food_kcal=int(data.getlist('p_price')[i]),
                food_cnt=int(foodcnt[i])
            )
            i+=1
        return redirect("/main/lunch/")
    getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=2)
    sum=0
    kcal=[0]
    cnt=0
    amount=0
    for food in getFood:
        sum+=food.food_kcal*food.food_cnt
        kcal.append(food.food_kcal*food.food_cnt)
        cnt+=food.food_cnt
        amount+=1
    return render(request, 'thirdeyes/mfoodedit.html',{'foods':getFood,'sum':sum,'kcal':kcal,'cnt':cnt,'amount':amount})

def dfoodedit(request):
    if request.method=="POST":
        data=request.POST
        i=0
        getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=3)
        getFood.delete()
        foodnames=data.getlist('food_name')[0].split(",")
        foodcnt=data.getlist('foodcnt')[0].split(",")
        while i<len(data.getlist('p_price')):
            UserFood.objects.create(
                id=request.session['id'],
                dt=request.session['date'],
                meal_type=3,
                food_name=foodnames[i],
                food_kcal=int(data.getlist('p_price')[i]),
                food_cnt=int(foodcnt[i])
            )
            i+=1
        return redirect("/main/dinner/")
    getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=3)
    sum=0
    kcal=[0]
    cnt=0
    amount=0
    for food in getFood:
        sum+=food.food_kcal*food.food_cnt
        kcal.append(food.food_kcal*food.food_cnt)
        cnt+=food.food_cnt
        amount+=1
    return render(request, 'thirdeyes/mfoodedit.html',{'foods':getFood,'sum':sum,'kcal':kcal,'cnt':cnt,'amount':amount})

def sfoodedit(request):
    if request.method=="POST":
        data=request.POST
        i=0
        getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=4)
        getFood.delete()
        foodnames=data.getlist('food_name')[0].split(",")
        foodcnt=data.getlist('foodcnt')[0].split(",")
        while i<len(data.getlist('p_price')):
            UserFood.objects.create(
                id=request.session['id'],
                dt=request.session['date'],
                meal_type=4,
                food_name=foodnames[i],
                food_kcal=int(data.getlist('p_price')[i]),
                food_cnt=int(foodcnt[i])
            )
            i+=1
        return redirect("/main/snack/")
    getFood=UserFood.objects.filter(id=request.session['id'],dt=request.session['date'],meal_type=4)
    sum=0
    kcal=[0]
    cnt=0
    amount=0
    for food in getFood:
        sum+=food.food_kcal*food.food_cnt
        kcal.append(food.food_kcal*food.food_cnt)
        cnt+=food.food_cnt
        amount+=1
    return render(request, 'thirdeyes/mfoodedit.html',{'foods':getFood,'sum':sum,'kcal':kcal,'cnt':cnt,'amount':amount})

# Create your views here. 

class ThirdeyesListAPI(APIView):
    def get(self, request):
        queryset = Thirdeyes.objects.all()
        print(queryset)
        serializer = ThirdeyesSerializer(queryset, many=True)
        return Response(serializer.data)