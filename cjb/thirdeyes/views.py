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
        inputId=data['id']
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
                request.session['id']=data['id']
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
        if getUser.gender==1:
                value=((13.7516*getUser.weight)+(5.0033*getUser.height)-(6.7550*getUser.age)+66.4730)*(1+(float(getUser.activity)))
        return render(request, 'thirdeyes/main.html',{'content':value, 'eats':get})
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
            if UserTb.objects.filter(id=data['id']).exists():
                context={
                    "result": "이미 존재하는 아이디입니다."
                }
            else:
                UserTb.objects.create(
                    id=data['id'],
                    pw=encoded_pw,
                    nm=data['nm'],
                    tel=data['tel'],
                    email=data['email']
                )
                LoginTb.objects.create(
                    user_id=data['id'],
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
    return render(request, 'thirdeyes/lunch.html')

def dinner(request):
    return render(request, 'thirdeyes/dinner.html')

def morning(request):
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date'])
    return render(request, 'thirdeyes/morning.html',{'foods':getFood})

def snack(request):
    return render(request, 'thirdeyes/snack.html')

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
    requestId=request.session['id']
    getFood=Food.objects.all()
    dt=date.today()
    dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
    if request.method=="POST":
        data=request.POST
        '''
        if UserFood.objects.filter(id=requestId,dt=dt2,meal_type=1).exists():
            getUser=UserFood.objects.get(id=requestId,dt=dt2,meal_type=1)
            getUser.food_name=data['food_name']
            getUser.food_kcal=int(data['food_kcal'])
            getUser.save()
        else:'''
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal'])
        )
        return redirect('/main/morning/')
    return render(request, 'thirdeyes/msearch.html', {'foods':getFood, 'id':request.session['id'],'date':dt2})

def lsearch(request):
    requestId=request.session['id']
    getFood=Food.objects.all()
    dt=date.today()
    dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        if UserFood.objects.filter(id=requestId,dt=dt2,meal_type=2).exists():
            getUser=UserFood.objects.get(id=requestId,dt=dt2,meal_type=2)
            getUser.food_name=data['food_name']
            getUser.food_kcal=int(data['food_kcal'])
            getUser.save()
        else:
            UserFood.objects.create(
                id=data['id'],
                dt=data['dt'],
                meal_type=2,
                food_name=data['food_name'],
                food_kcal=int(data['food_kcal'])
            )
        return redirect('/main/lunch/')
    return render(request, 'thirdeyes/lsearch.html', {'foods':getFood, 'id':request.session['id'],'date':dt2})

def dsearch(request):
    requestId=request.session['id']
    getFood=Food.objects.all()
    dt=date.today()
    dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        if UserFood.objects.filter(id=requestId,dt=dt2,meal_type=3).exists():
            getUser=UserFood.objects.get(id=requestId,dt=dt2,meal_type=3)
            getUser.food_name=data['food_name']
            getUser.food_kcal=int(data['food_kcal'])
            getUser.save()
        else:
            UserFood.objects.create(
                id=data['id'],
                dt=data['dt'],
                meal_type=3,
                food_name=data['food_name'],
                food_kcal=int(data['food_kcal'])
            )
        return redirect('/main/dinner/')
    return render(request, 'thirdeyes/dsearch.html', {'foods':getFood, 'id':request.session['id'],'date':dt2})

def ssearch(request):
    requestId=request.session['id']
    getFood=Food.objects.all()
    dt=date.today()
    dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        if UserFood.objects.filter(id=requestId,dt=dt2,meal_type=4).exists():
            getUser=UserFood.objects.get(id=requestId,dt=dt2,meal_type=4)
            getUser.food_name=data['food_name']
            getUser.food_kcal=int(data['food_kcal'])
            getUser.save()
        else:
            UserFood.objects.create(
                id=data['id'],
                dt=data['dt'],
                meal_type=4,
                food_name=data['food_name'],
                food_kcal=int(data['food_kcal'])
            )
        return redirect('/main/snack/')
    return render(request, 'thirdeyes/ssearch.html', {'foods':getFood, 'id':request.session['id'],'date':dt2})

# Create your views here. 

class ThirdeyesListAPI(APIView):
    def get(self, request):
        queryset = Thirdeyes.objects.all()
        print(queryset)
        serializer = ThirdeyesSerializer(queryset, many=True)
        return Response(serializer.data)