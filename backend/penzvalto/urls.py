from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('restadat/', views.restAdatKezeles, name='restAdatKezeles'),
    path('logout/',views.logout_user, name='logout'),
    path('signup/',views.signup_page, name='signup'),
    path('delete/',views.delete_user,name="deleteuser")
    ]