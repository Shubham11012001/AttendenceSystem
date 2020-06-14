from django import forms
from .models import UserDetails, Attendence , Department

#creating userform for signing up..!!
class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = [
            'userName',
            'userIp',
            'userDepartment',
        ]


class loginForm(forms.Form):
    username =  forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 20)


class AttendenceForm(forms.Form):
    date = forms.DateField()
    time = forms.TimeField()
    ip = forms.GenericIPAddressField()
    latitude = forms.CharField()
    longitude = forms.CharField()
    