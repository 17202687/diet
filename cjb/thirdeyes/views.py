from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages


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
    return render(request, 'thirdeyes/user.html')

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
