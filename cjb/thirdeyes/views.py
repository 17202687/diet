from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'thirdeyes/login.html')

def main(request):
    return render(request, 'thirdeyes/main.html')

def set(request):
    return render(request, 'thirdeyes/set.html')

def signup(request):
    return render(request, 'thirdeyes/signup.html')

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

def search(request):
    return render(request, 'thirdeyes/search.html')