from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import *
from django.shortcuts import redirect

def isActive(moduleType,userType):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            module = Form.objects.get(name=moduleType)
            if userType == 'student':
                student = StudentsInfo.objects.get(user = request.user)                            
            if FormDetails.objects.filter(form=module,open=True,teacher=student.teacher).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/forbidden')
        return wrap
    return decorator