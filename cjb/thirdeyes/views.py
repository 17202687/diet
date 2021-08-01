from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone


# Create your views here.

def login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        data=request.POST
        inputId=data['id']
        inputPw=data['pw']
        if UserTb.objects.filter(id=data['id']).exists():
            getUser=UserTb.objects.get(id=inputId)
            if(getUser.pw == inputPw):
                #로그인 성공
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
    if UserInfo.objects.filter(user_id=requestId).exists():
        getUser=UserInfo.objects.get(user_id=requestId)
        get=UserFood.objects.filter(id=requestId)
        if getUser.gender==1:
                value=((13.7516*getUser.weight)+(5.0033*getUser.height)-(6.7550*getUser.age)+66.4730)*(1+(float(getUser.activity)))
        return render(request, 'thirdeyes/main.html',{'content':value, 'eats':get})
    return render(request, 'thirdeyes/main.html') 

def set(request):
    return render(request, 'thirdeyes/set.html')

def signup(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            data=request.POST
            #id_value=data['id']#form.cleaned_data.get('id')
            if UserTb.objects.filter(id=data['id']).exists():
                context={
                    "result": "이미 존재하는 아이디입니다."
                }
            else:
                form.save()
                LoginTb.objects.create(
                    user_id=data['id'],
                    pw=data['pw']
                )
                return redirect('/')
    else:
        form = MyForm()
    return render(request, 'thirdeyes/signup.html', {'form': form})

def user(request):
    requestId=request.session['id']
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
    return render(request, 'thirdeyes/morning.html')

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
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal'])
        )
        return redirect('/')
    return render(request, 'thirdeyes/msearch.html', {'foods':getFood, 'id':request.session['id']})

def lsearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal'])
        )
        return redirect('/')
    return render(request, 'thirdeyes/lsearch.html', {'foods':getFood, 'id':request.session['id']})

def dsearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal'])
        )
        return redirect('/')
    return render(request, 'thirdeyes/dsearch.html', {'foods':getFood, 'id':request.session['id']})

def ssearch(request):
    getFood=Food.objects.all()
    if request.method=="POST":
        data=request.POST
        print(data['id'])
        UserFood.objects.create(
            id=data['id'],
            dt=data['dt'],
            meal_type=data['meal_type'],
            food_name=data['food_name'],
            food_kcal=int(data['food_kcal'])
        )
        return redirect('/')
    return render(request, 'thirdeyes/ssearch.html', {'foods':getFood, 'id':request.session['id']})

# Create your views here. 