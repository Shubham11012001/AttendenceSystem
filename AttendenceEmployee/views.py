from django.shortcuts import render, redirect, reverse
from .models import UserDetails,Attendence , Department, TotalAttendence
from .forms import UserDetailsForm,loginForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from math import radians, cos, sin, asin, sqrt
import random,time
import string
from userRecognition.featureExctrection import *
from userRecognition.makedirtakeaudio import *
from userRecognition.test import *
from userRecognition.training import *
from .call_me_twilio import *
from datetime import date 


#getting distance between two points
def distance(lat1, lon1, lat2, lon2): 
	# The math module contains a function named 
	# radians which converts from degrees to radians. 
	lon1 = radians(lon1) 
	lon2 = radians(lon2) 
	lat1 = radians(lat1) 
	lat2 = radians(lat2) 
	# Haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * asin(sqrt(a)) 
	# Radius of earth in kilometers. Use 3956 for miles 
	r = 6371
    # calculate the result 
	return(c * r) 



#for generating privacy key
def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size)) #generating key and returning it


def takeRandomKey():
    chars = string.ascii_letters + string.digits  #using alphabets and letters
    size = 6 #length of key!!!
    return random_string_generator(size, chars)


# Create your views here.
def check(request):
    current_user = request.user #for getting the current user, if there is the user
    if current_user:
        return render(request,'index.html',{'context':current_user})
    else:
        return render(request,'index.html')




def registerView(request):
    if request.method == "POST":
        user_name = request.POST['username']
        user_ip = request.POST['userIp']
        user_department = request.POST['userDepartment']
        userPrivacyKey = takeRandomKey()
        print(userPrivacyKey)
        user_password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        user = User(username = user_name)
        user.set_password(user_password)
        if User.objects.filter(username = user_name).exists():
            messages.success(request,"UserName already exists")
            return HttpResponse("Try Again Please, That username already exists")
        elif user_password != confirm_password:
            messages.success(request,"Password not matched")
            return HttpResponse("Try Again Please, Password was not matched")
        else:
            user.save()
            try:
                details = UserDetails()
                details.user = user
                details.userName = user_name
                details.userIp = user_ip
                details.userDepartment = user_department
                details.userPassword = user_password
                details.userPrivacyKey = userPrivacyKey
                details.save()
                totalAttendence = TotalAttendence()
                totalAttendence.user = user
                totalAttendence.month = 1
                totalAttendence.countAttendence=0
                totalAttendence.save()
                response = redirect('login')
                response.set_cookie('Private_Key',userPrivacyKey)
                return response
            except:
                a = User.objects.get(username = user_name)
                a.delete()
                return HttpResponse("<h1>There is a internal server error</h1>")
    else:
        form = UserDetailsForm
        return render(request,'registerForm.html',{'form':form})

def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username = username)
            password = request.POST['password']
            print(username,password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            #userdetails = UserDetails.objects.get(user = User.objects.get(username = username))
            print(user,password)
            user = authenticate(username = username,password = password)
            if user is not None:
                if user.is_active:
                    print("Active")
                    login(request,user)
                    return redirect('attendence')
                else:
                    print("Error")
                    messages.success(request,"Please check entered ID and Passwored, because something went wrong!!")
                    return reverse('login')
        except:
            messages.success(request,"User not found")
            return redirect('login')
    else:
        form = loginForm
        return render(request,'login.html',{'form':form})


def logoutView(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('/')



@login_required
def markingAttendence(request):
    try:
        username = request.user
        if request.method == "POST":
            models =Attendence()
            sec_models = TotalAttendence.objects.get(user = username)
            if 'Private_Key' in request.COOKIES:
                privateKey = request.COOKIES['Private_Key']
            else:
                privateKey = False
                print(privateKey)
            date = request.POST['date']
            time = request.POST['time']
            request_ip = request.POST['ip']
            user_lat = request.POST['latitude']
            user_lat = float(user_lat)
            user_lon = request.POST['longitude']
            user_lon = float(user_lon)
            print(username,user_lat,user_lon,request_ip,time,date)
            gettingUser = User(username = username)
            usermodel = UserDetails.objects.get(user = User.objects.get(username = username))
            print(usermodel.userPrivacyKey) 
            department = usermodel.userDepartment
            print(department)
            departmentalmodel = Department.objects.get(departmentName = department)
            departmentIp = departmentalmodel.departmental_ip
            departmentLatitude = float(departmentalmodel.departmental_lat)
            departmentLongitude = float(departmentalmodel.departmental_lon)
            distance_number = distance(departmentLatitude,departmentLongitude,user_lat,user_lon)
            print(distance_number)
            print(type(distance_number))
            print(int(distance_number))
            if request_ip == departmentIp:
                models.userDetails = usermodel
                models.dateField = date
                models.timeField = time
                models.wasPresent = True
                month =date.split("-")
                sec_models.month=month[1]
                sec_models.countAttendence+=1
                sec_models.save()
                models.save()
                return HttpResponse("Marked Attended")
            else:
                if request_ip == usermodel.userIp:
                    if distance_number < 2:
                        models.userDetails = usermodel
                        models.dateField = date
                        models.timeField = time
                        models.wasPresent = True
                        month =date.split("-")
                        sec_models.month=month[1]
                        sec_models.countAttendence+=1
                        sec_models.save()
                        models.save()
                        messages.success(request,"Attendence Marked")
                        return render(request,"Thankyou.html")
                    else:
                        #return HttpResponse("You are far away from your Departmental Location")
                        messages.success(request,"You are far away from your DEPARTMENTAL LOCATION")
                        return redirect("thankyou")
                elif privateKey:
                    if privateKey == usermodel.userPrivacyKey:
                        if distance_number< 2:
                            models.userDetails = usermodel
                            models.dateField = date
                            models.timeField = time
                            models.wasPresent = True
                            month =date.split("-")
                            sec_models.month=month[1]
                            sec_models.countAttendence+=1
                            sec_models.save()
                            models.save()
                            #return HttpResponse("Marked Attended")
                            messages.success(request,"Maked Arrendence")
                            return redirect('thankyou')
                        else:
                            #return HttpResponse("You are far away from your Departmental Location")
                            messages.success(request,"You are far away from your DEPARTMENTAL LOCATION")
                            return redirect('thankyou')
                else:
                    #return HttpResponse("Your IP have not matched and not Cookies are favourable")
                    messages.success(request,"Your IP have not matched and Cache haven't matched")
                    return redirect('thankyou')
        else:
            form = Attendence
            model = UserDetails.objects.get(user = request.user)
            return render(request,'attendenceform.html',{'form':form,'model':model})
    except Exception:
        messages.success(request,"Something went wrong")
        return redirect('login')

@login_required
def training_view(request):
    model = UserDetails.objects.get(user = request.user)
    return render(request,"registeryourvoice.html",{'model':model})


@login_required
def train_model_for_voice(request):
    try:
        username = str(request.user)
        print(username)
        makeDirector(username)
        for i in range(0,15):
            recordaudio(username,i)
        training_data(username)
        messages.success(request,"We have recorded your voice. Thank you!!")
        return render(request,'registeryourvoice.html')
    except Exception:
        messages.success(request,"We have faced an error while Training our machine. Please try again later")
        return redirect('trainingpage')
    
def call_me(request):
    calling_user()
    return HttpResponse("<h1> Please Pick Up call <h1>")


@login_required
def testvoiceHere(request):
    username = str(request.user)
    usermodel = UserDetails.objects.get(user = User.objects.get(username= username))
    models = Attendence()
    datee = date.today()
    curr_time = time.localtime() 
    x= testing_recordaudio(username)
    print(usermodel)
    print(x)
    if x == username:
        models.userDetails = usermodel
        models.wasPresent = True
        models.save()
        messages.success(request,"Attendence Marked")
        return redirect('thankyou')
    else:
        messages.success(request,"Your voice have not matched")
        return redirect('thankyou')

def thankyou(request):
    return render(request,"Thankyou.html")