from django.urls import path  
from registration import views  
urlpatterns = [      
    # path('',views.show),
    # path('submit',views.show),
    # path('get/',views.get),
    # path('getExcel/',views.getExcel),
    # path('excelRegister/',views.excelRegister),
    path('consent/',views.consent),
    path('home/',views.home),
    path('parents_info/',views.parents_info),
    path('students_info/',views.students_info),
    path('parent_login/',views.parent_login),
    path('bulkRegister/',views.bulkRegister),
    path('getTemplate/',views.getTemplate),
    path('downloadData/',views.downloadData),
    
]  