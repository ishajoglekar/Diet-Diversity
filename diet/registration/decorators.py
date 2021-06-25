from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import *
from django.shortcuts import redirect


def isActive(moduleType,userType):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            module = Form.objects.get(name=moduleType) 
            if not 'parent_dashboard' in request.build_absolute_uri().split('/'):
                student = StudentsInfo.objects.get(user = request.user)    
                if FormDetails.objects.filter(form=module,open=True,teacher=student.teacher).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('/form_closed')

            elif 'parent_dashboard' in request.build_absolute_uri().split('/'):
                studentID = request.META.get('HTTP_REFERER').split('/')[-2]
                student = ParentsInfo.objects.filter(user= request.user).first().studentsinfo_set.get(pk=studentID)
            
                if FormDetails.objects.filter(form=module,open=True,teacher=student.teacher).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('/form_closed')

        return wrap
    return decorator