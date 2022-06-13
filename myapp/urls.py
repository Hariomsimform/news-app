from django.urls import path
from .views import logout_reqest, register, login, home, user_profile, task_mail
urlpatterns = [
    path('', register, name='register' ),
    path('login/',login, name='login'),
    path('home/',home, name='home'),
    path('user-profile/', user_profile, name='user-profile'),
    path('logout/', logout_reqest, name='logout-request'),
    path('reload/', task_mail, name='reload')  

]