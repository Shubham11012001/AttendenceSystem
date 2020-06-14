from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Create your models here.
DEPARTMENTAL_CHOICE =(
    ('COMPUTER DEPARTMENT','COMPUTER DEPARTMENT'),
    ('ACCOUNTS DEPARTMENT','ACCOUNTS DEPARTMENT'),
    ('PRODUCTION DEPARTMENT','PRODUCTION DEPARTMENT'),
    ('MARKETING DEPARTMENT','MARKETING DEPARTMENT'),
    ('HR DEPARTMERT','HR DEPARTMERT'),
) 

class Department(models.Model):
    departmentName = models.CharField(max_length = 40)
    departmental_lat = models.CharField(max_length = 20)
    departmental_lon = models.CharField(max_length= 20)
    departmental_ip = models.GenericIPAddressField()


    def __str__(self):
        return self.departmentName

    

#For getting details from the user
class UserDetails(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    userName = models.CharField(max_length = 50, unique=True)
    userIp = models.GenericIPAddressField()
    userPassword = models.CharField(max_length = 30,blank= True)
    userDepartment = models.CharField(max_length = 50, choices=DEPARTMENTAL_CHOICE, default='COMPUTER DEPARTMENT')
    userPrivacyKey = models.CharField(max_length = 20,unique=True)  #we will generate this key for user identification

    def __str__(self):
        return self.userName



#Models for Marking attendence
class Attendence(models.Model):
    userDetails = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    dateField = models.DateField(default = datetime.date.today())
    timeField = models.TimeField(default = timezone.localtime(timezone.now()).time())
    wasPresent = models.BooleanField(default=False)

    def __str__(self):
        return 'Date:{}'.format(self.dateField)


#Models for getting count of Attendence of any user
class TotalAttendence(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    month = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(12),MinValueValidator(1)]
    )
    countAttendence = models.IntegerField(
        default = 0,
        validators=[MaxValueValidator(30)]
    )

    def __str__(self):
        return self.user.username

    



