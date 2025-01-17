from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('signup/',views.signup_page, name='signup'),
    path('restadat/', views.restAdatKezeles, name='restAdatKezeles'),
    path('logout/',views.logout_user, name='logout'),
    path('delete/',views.delete_user,name="deleteuser"),
    
    path('mnbvaluta/', views.restMNBValuta),
    path('mnbvalutalast/', views.restMNBValutaLast),
    path('mnbname/', views.restMNBName),
    path('mnbrefresh/', views.restMNBRefresh),
    ]