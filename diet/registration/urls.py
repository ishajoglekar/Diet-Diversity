from django.contrib import admin  
from django.urls import path  
from registration import views  
urlpatterns = [      
    path('',views.show),
    # path('submit',views.show),
    path('get/',views.get),
    path('getExcel/',views.getExcel),
    path('excelRegister/',views.excelRegister),
    path('consent/',views.consent),
    path('parents_info/',views.parents_info),
    path('students_info/',views.students_info)

]  