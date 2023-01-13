from django.contrib import admin
from django.urls import path,include
from mysite import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index),
    path('login/',views.Login.as_view()),
    path('logout/',LogoutView.as_view()), 
    path('blog/',include('blog.urls')),
    path('signup/',views.signup),
    path('mypage/',views.MypageView.as_view()),
    path('contact/',views.ContactView.as_view()),
    path('pay/',views.Payview.as_view()),
]