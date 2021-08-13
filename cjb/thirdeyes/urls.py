from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from thirdeyes.views import ThirdeyesListAPI

urlpatterns = [
    path('', views.login, name='login'),
    path('main/', views.main, name='main'),
    path('main/set/', views.set, name='set'),
    path('signup/', views.signup, name='signup'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('main/set/user/', views.user, name='user'),
    path('main/morning/', views.morning, name='morning'),
    path('main/lunch/', views.lunch, name='lunch'),
    path('main/dinner/', views.dinner, name='dinner'),
    path('main/snack/', views.snack, name='snack'),
    path('main/set/alarm/', views.alarm, name='alarm'),
    path('main/diary/', views.diary, name='diary'),
    path('main/set/alarm/malarm/', views.malarm, name='malarm'),
    path('main/set/alarm/lalarm/', views.lalarm, name='lalarm'),
    path('main/set/alarm/dalarm/', views.dalarm, name='dalarm'),
    path('main/morning/msearch/', views.msearch, name='msearch'),
    path('main/lunch/lsearch/', views.lsearch, name='lsearch'),
    path('main/dinner/dsearch/', views.dsearch, name='dsearch'),
    path('main/snack/ssearch/', views.ssearch, name='ssearch'),
    path('main/morning/mfoodedit', views.mfoodedit, name='mfoodedit'),
    path('main/lunch/lfoodedit', views.lfoodedit, name='lfoodedit'),
    path('main/dinner/dfoodedit', views.dfoodedit, name='dfoodedit'),
    path('main/snack/sfoodedit', views.sfoodedit, name='sfoodedit'),
    path('main/activity', views.activity, name='activity'),
    path('main/activity/activityedit', views.activityedit, name='activityedit'),
    path('admin/', admin.site.urls), path('api/thirdeyes/', ThirdeyesListAPI.as_view()),
    #path('checks/', include('checks.urls')),
    #path('rest-auth/', include('rest_auth.urls')),
    path('users/', include('api_user.urls'), name='api_user'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
