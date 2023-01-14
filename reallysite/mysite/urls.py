from django.urls import path
from mysite import views
from django.contrib.auth.views import LogoutView


app_name = "mysite"

urlpatterns = [
    path('',views.index,name="home"),
    path('landing/',views.landing,name="landing"),
    path('login/',views.Login.as_view()),
    path('logout/',LogoutView.as_view()), 
    path('signup/',views.signup),
    path('mypage/',views.MypageView.as_view()),
    path('contact/',views.ContactView.as_view()),
    path('pay/',views.Payview.as_view()),

    path('ping/',views.ping),
]