from django.contrib import admin

from .models import ParentsInfo,StudentsInfo,TeacherInCharge,State,City


admin.site.register(ParentsInfo)
admin.site.register(StudentsInfo)
admin.site.register(TeacherInCharge)
admin.site.register(State)
admin.site.register(City)

# Register your models here.
