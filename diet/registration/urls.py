from django.urls import path  
from registration import views  
urlpatterns = [      
    path('',views.loginU),
    # path('submit',views.show),
    # path('get/',views.get),
    # path('getExcel/',views.getExcel),
    # path('excelRegister/',views.excelRegister),
    path('consent/',views.consent),
    path('home/',views.home),
    path('parents_info/',views.parents_info),
    path('students_info/',views.students_info),
    path('login/',views.loginU),
    path('bulkRegister/',views.bulkRegister),
    path('getTemplate/',views.getTemplate),
    path('downloadData/',views.downloadData),
    path('parent_dashboard/',views.dashboard),
    path('student_dashboard/',views.student_dashboard),
    path('teacher_dashboard/',views.teacher_dashboard),
    path('logout/',views.logoutU),
    path('addStudentForm/',views.addStudentForm),
    # path('firstModule/',views.getFirstModule),
    # path('nutri/',views.nutri),
    # path('nutriPartTwo/',views.nutriPartTwo),
    path('moduleOne/',views.moduleOne),
    path('moduleOne-2/',views.moduleOne2),
    path('moduleOne-3/',views.moduleOne3),
    path('draft/',views.draft),
    path('forbidden/',views.forbidden)
]
  