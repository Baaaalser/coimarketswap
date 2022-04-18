from django.urls import path, include
from .views import LoginView, LogoutView, SignupView,UsersList  #,ProfileView

urlpatterns = [

     # Auth views
     path('auth/login/',
          LoginView.as_view(), name='auth_login'),

     path('auth/logout/',
          LogoutView.as_view(), name='auth_logout'),

     path('auth/signup/',
          SignupView.as_view(), name='auth_signup'),
     path('auth/showusers',UsersList.as_view(),name='auth_showusers')


]