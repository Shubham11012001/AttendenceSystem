from django.contrib import admin
from .models import Attendence,UserDetails,TotalAttendence,Department


# Register your models here.
admin.site.register(UserDetails)
admin.site.register(Department)
admin.site.register(Attendence)
admin.site.register(TotalAttendence)
