from django.contrib import admin

from .models import ParentsInfo,StudentsInfo,TeacherInCharge


admin.site.register(ParentsInfo)
admin.site.register(StudentsInfo)
admin.site.register(TeacherInCharge)

# Register your models here.
