from django.shortcuts import render
from .models import Register

# Create your views here.
def show(request):
    print(request.method)
    if(request.method=="POST"):
        name = request.POST['name']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        facilities1 = request.POST['priority']
        facilities2 = request.POST['priority1']
        facilities3 = request.POST['priority2']
        sports = request.POST.getlist('priority3[]')
        print(sports)
        my_string = ','.join(sports)
        print(my_string)
        r = Register(name=name,age=age,height=height,weight=weight,facilities1=facilities1,facilities2=facilities2,facilities3=facilities3,sports=my_string)
        r.save()
    return render(request,'index.html')