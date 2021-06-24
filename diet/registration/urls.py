from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView  
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
    path('teacher_dashboard/<int:id>/',views.getFormDetails),
    path('logout/',views.logoutU),
    path('addStudentForm/',views.addStudentForm),
    # path('firstModule/',views.getFirstModule),
    # path('nutri/',views.nutri),
    # path('nutriPartTwo/',views.nutriPartTwo),
    path('moduleOne/',views.moduleOne),
    path('moduleOne-2/',views.moduleOne2),
    path('moduleOne-3/',views.moduleOne3),
    path('draft/',views.draft),
    path('forbidden/',views.forbidden),
    path('parent_dashboard/<int:id>/',views.showStudent),
    path('parent_dashboard/<int:id>/moduleOne',views.parentModuleOne),
    path('parent_dashboard/<int:id>/moduleOne-2',views.parentModuleOne2,name='parentsModuleOne2'),
    path('parent_dashboard/<int:id>/moduleOne-3',views.parentModuleOne3,name='parentsModuleOne3'),
    path('previous/',views.previous),
    path('manage-forms/',views.manageForms),

    # path('404notFound/',views.unmatched),
    # path(r'*', 'views.unmatched'),
    # url(r'^.*$', RedirectView.as_view(url='/404notFound/', permanent=False), name='index')
]
  