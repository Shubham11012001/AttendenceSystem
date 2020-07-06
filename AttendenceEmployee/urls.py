from django.urls import path
from . import views
from django.conf.urls import url
#from AttendenceEmployee.views import *


#writing our own url patterns
urlpatterns=[
    path('',views.check,name='index'),
    path('register/',views.registerView,name="register"),
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView,name = 'logout'),
    path('login/attendence/',views.markingAttendence, name='attendence'),
    path('trainingpage/',views.training_view,name="trainingpage"),
    path('recordingaudio/',views.train_model_for_voice,name="recordingaudio"),
    path('callme/',views.call_me,name="callme"),
    path('thankyou',views.thankyou,name="thankyou"),
    path('testvoice/',views.testvoiceHere,name="testvoice")
]