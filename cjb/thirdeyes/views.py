from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from datetime import date,datetime, timedelta
import bcrypt
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ThirdeyesSerializer
from django.utils.dateparse import parse_date

# Create your views here.

def login(request):
    try:
        if(request.session['autologin']==1 and request.session['id']!=""):
            dt=date.today()
            dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
            request.session['date']=dt2
            return redirect('main/')
    except:
        a="1"
    if request.method=="POST":
        form = LoginForm(request.POST)
        data=request.POST
        inputId=data['email']
        inputPw=data['pw']
        hashed_pw=bcrypt.hashpw(inputPw.encode('utf-8'),bcrypt.gensalt())
        encoded_pw=hashed_pw.decode('utf-8')
        if UserTb.objects.filter(email=data['email']).exists():
            getUser=UserTb.objects.get(email=inputId)
            #if(getUser.pw == inputPw):
            if(bcrypt.checkpw(inputPw.encode('utf-8'),getUser.pw.encode('utf-8'))):
                #로그인 성공
                try:
                    data['autologin']
                    request.session['autologin']=1
                except:
                    request.session['autologin']=0
                dt=date.today()
                dt2=str(dt.year)+"-"+str(dt.month)+"-"+str(dt.day)
                request.session['date']=dt2
                request.session['id']=data['email']
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
    datearray=[]
    datearray.append(parse_date(request.session['date']).weekday())
    if(request.method=="POST"):
        data=request.POST
        if(data['logout']=="1"):
            request.session['id']=""
            return redirect('/')
        datearray=data['selectedday'].split()

        if(datearray[1]=="Jan"):
            mon="01"
        elif(datearray[1]=="Feb"):
            mon="02"
        elif(datearray[1]=="Mar"):
            mon="03"
        elif(datearray[1]=="Apr"):
            mon="04"
        elif(datearray[1]=="May"):
            mon="05"
        elif(datearray[1]=="Jun"):
            mon="06"
        elif(datearray[1]=="Jul"):
            mon="07"
        elif(datearray[1]=="Aug"):
            mon="08"
        elif(datearray[1]=="Sep"):
            mon="09"
        elif(datearray[1]=="Oct"):
            mon="10"
        elif(datearray[1]=="Nov"):
            mon="11"
        elif(datearray[1]=="Dec"):
            mon="12"
        day=datearray[2]
        year=datearray[3]
        selectedday=year+"-"+mon+"-"+day
        request.session['date']=selectedday

    if(datearray[0]=="Mon" or datearray[0]==0):
        dy=0
    elif(datearray[0]=="Tue" or datearray[0]==1):
        dy=1
    elif(datearray[0]=="Wed" or datearray[0]==2):
        dy=2
    elif(datearray[0]=="Thu" or datearray[0]==3):
        dy=3
    elif(datearray[0]=="Fri" or datearray[0]==4):
        dy=4
    elif(datearray[0]=="Sat" or datearray[0]==5):
        dy=5
    elif(datearray[0]=="Sun" or datearray[0]==6):
        dy=6
    i=7
    kcalsum=[]
    actkcal=[]
    while i>0:
        tmpdt=parse_date(request.session['date'])-timedelta(i+dy-7)
        tmpFood=UserFood.objects.filter(id=request.session['id'],dt=tmpdt)
        tmpAct=UserActivity.objects.filter(id=request.session['id'],dt=tmpdt)
        kcsum=0
        for food in tmpFood:
            kcsum+=food.food_kcal*food.food_cnt
        kcalsum.append(kcsum)

        actkc=0
        for act in tmpAct:
            actkc+=float(act.act_kcal)
        actkcal.append(actkc)
        i-=1
    requestId=request.session['id']
    mUrl=""
    lUrl=""
    dUrl=""
    sUrl=""
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=1,dt=request.session['date'])
        mUrl=getImg.img.url
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=2,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=2,dt=request.session['date'])
        lUrl=getImg.img.url
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=3,dt=request.session['date'])
        dUrl=getImg.img.url
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=4,dt=request.session['date'])
        sUrl=getImg.img.url
    if UserInfo.objects.filter(user_id=requestId).exists():
        getUser=UserInfo.objects.get(user_id=requestId)
        msum=0
        lsum=0
        dsum=0
        ssum=0
        sum=0
        get=UserFood.objects.filter(id=requestId,dt=request.session['date'],meal_type=1)
        for a in get:
            msum+=a.food_kcal*a.food_cnt
        get=UserFood.objects.filter(id=requestId,dt=request.session['date'],meal_type=2)
        for a in get:
            lsum+=a.food_kcal*a.food_cnt
        get=UserFood.objects.filter(id=requestId,dt=request.session['date'],meal_type=3)
        for a in get:
            dsum+=a.food_kcal*a.food_cnt
        get=UserFood.objects.filter(id=requestId,dt=request.session['date'],meal_type=4)
        for a in get:
            ssum+=a.food_kcal*a.food_cnt
        sum=msum+lsum+dsum+ssum
        if getUser.gender==1:
            value=((13.7516*getUser.weight)+(5.0033*getUser.height)-(6.7550*getUser.age)+66.4730)*(1+(float(getUser.activity)))
        dtsplit=request.session['date'].split("-")
        getAct=UserActivity.objects.filter(id=request.session['id'],dt=request.session['date'])
        actsum=0
        for act in getAct:
            actsum+=act.act_kcal
        return render(request, 'thirdeyes/main.html',{'content':value,'actsum':int(actsum), 'monact':actkcal[0],'tueact':actkcal[1],'wedact':actkcal[2],'thuact':actkcal[3],'friact':actkcal[4],'satact':actkcal[5],'sunact':actkcal[6],'eats':get, 'sum':sum, 'username':UserTb.objects.get(email=request.session['id']).nm,'mUrl':mUrl, 'lUrl':lUrl,'dUrl':dUrl,'sUrl':sUrl,'msum':msum,'lsum':lsum,'dsum':dsum,'ssum':ssum,'month':str(int(dtsplit[1])-1),'day':dtsplit[2],'year':dtsplit[0],'monsum':kcalsum[0],'tuesum':kcalsum[1],'wedsum':kcalsum[2],'thusum':kcalsum[3],'frisum':kcalsum[4],'satsum':kcalsum[5],'sunsum':kcalsum[6]})
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
            if UserTb.objects.filter(email=data['email']).exists():
                context={
                    "result": "이미 존재하는 아이디입니다."
                }
            else:
                UserTb.objects.create(
                    nm=data['name'],
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

def forgotpassword(request):
    return render(request, 'thirdeyes/forgotpassword.html')    

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
            return redirect('/main/')
        else:
            UserInfo.objects.create(
                user_id=requestId,
                gender=data['gender'],
                age=data['age'],
                height=data['height'],
                weight=data['weight'],
                activity=data['activity']
            )
            return redirect('/main/')
    else:
        form=LoginForm()
    return render(request, 'thirdeyes/user.html',{'forms':form, 'context':value})

def lunch(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            if request.POST['image_del']=="del":
                delFood=FoodImage.objects.filter(id=request.session['id'],meal_type=2,dt=request.session['date'])
                delFood.delete()
            try:
                img=request.FILES["image_field"]
            except:
                return redirect('/main/')
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
            return redirect('/main/')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=2,dt=request.session['date'])
    i=0
    while i<len(getFood):
        getFood[i].sum=getFood[i].food_kcal*getFood[i].food_cnt
        i+=1
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=2,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=2,dt=request.session['date'])
        getUrl=getImg.img.url
        return render(request, 'thirdeyes/lunch.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/lunch.html',{'foods':getFood})

def dinner(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            if request.POST['image_del']=="del":
                delFood=FoodImage.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date'])
                delFood.delete()
            try:
                img=request.FILES["image_field"]
            except:
                return redirect('/main/')
            img=request.FILES["image_field"]
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
            return redirect('/main/')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date'])
    i=0
    while i<len(getFood):
        getFood[i].sum=getFood[i].food_kcal*getFood[i].food_cnt
        i+=1
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=3,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=3,dt=request.session['date'])
        getUrl=getImg.img.url
        return render(request, 'thirdeyes/dinner.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/dinner.html',{'foods':getFood})

def morning(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            if request.POST['image_del']=="del":
                delFood=FoodImage.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date'])
                delFood.delete()
            try:
                img=request.FILES["image_field"]
            except:
                return redirect('/main/')
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
            return redirect('/main/')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date'])
    i=0
    while i<len(getFood):
        getFood[i].sum=getFood[i].food_kcal*getFood[i].food_cnt
        i+=1
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=1,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=1,dt=request.session['date'])
        getUrl=getImg.img.url
        return render(request, 'thirdeyes/morning.html',{'foods':getFood,'img':getUrl})
    return render(request, 'thirdeyes/morning.html',{'foods':getFood})

def snack(request):
    if request.method=="POST":
        form=foodImageForm(request.POST, request.FILES)
        if form.is_valid:
            if request.POST['image_del']=="del":
                delFood=FoodImage.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date'])
                delFood.delete()
            try:
                img=request.FILES["image_field"]
            except:
                return redirect('/main/')
            img=request.FILES["image_field"]
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
            return redirect('/main/')
    getFood=UserFood.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date'])
    i=0
    while i<len(getFood):
        getFood[i].sum=getFood[i].food_kcal*getFood[i].food_cnt
        i+=1
    if(FoodImage.objects.filter(id=request.session['id'],meal_type=4,dt=request.session['date']).exists()):
        getImg=FoodImage.objects.get(id=request.session['id'],meal_type=4,dt=request.session['date'])
        getUrl=getImg.img.url
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
            meal_type=2,
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
            meal_type=3,
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
            meal_type=4,
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

def activity(request):
    getAct=UserActivity.objects.filter(id=request.session['id'],dt=request.session['date'])
    sumkcal=0
    for act in getAct:
        sumkcal+=act.act_kcal
    if request.method=="POST":
        data=request.POST
        kcal=float(data['selected'])*float(data['minutes'])*UserInfo.objects.get(user_id=request.session['id']).weight*3.5*0.005
        UserActivity.objects.create(
            id=request.session['id'],
            dt=request.session['date'],
            act_name=data['act_name'],
            act_met=float(data['selected']),
            act_time=data['minutes'],
            act_kcal=kcal
        )
        getAct=UserActivity.objects.filter(id=request.session['id'],dt=request.session['date'])
        sumkcal=0
        for act in getAct:
            sumkcal+=act.act_kcal
        return render(request, 'thirdeyes/activity.html',{'kcal':kcal, 'sumkcal':sumkcal})

    return render(request, 'thirdeyes/activity.html',{'kcal':0,'sumkcal':sumkcal})

def activityedit(request):
    getAct=UserActivity.objects.filter(id=request.session['id'],dt=request.session['date'])
    if request.method=="POST":
        data=request.POST
        getAct.delete()
        i=0
        while i<len(data.getlist('act_name')):
            tmpName=data.getlist('act_name')[i]
            if(tmpName==""):
                break
            tmpTime=data.getlist('act_time')[i]
            tmpMet=data.getlist('act_met')[i]
            UserActivity.objects.create(
                id=request.session['id'],
                dt=request.session['date'],
                act_name=tmpName,
                act_met=tmpMet,
                act_time=tmpTime,
                act_kcal=float(tmpMet)*float(tmpTime)*UserInfo.objects.get(user_id=request.session['id']).weight*3.5*0.005
            )
            i+=1
        return redirect('/main/activity/')

    return render(request,'thirdeyes/activityedit.html', {'getAct':getAct})
# Create your views here. 

class ThirdeyesListAPI(APIView):
    def get(self, request):
        queryset = Thirdeyes.objects.all()
        print(queryset)
        serializer = ThirdeyesSerializer(queryset, many=True)
        return Response(serializer.data)