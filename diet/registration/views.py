from django.shortcuts import render
from .models import Register
from registration.models import *
from django.contrib import messages
import environ
env = environ.Env()
environ.Env.read_env() 
from cryptography.fernet import Fernet

key: bytes = bytes(env('KEY'),'ascii')
f = Fernet(key)

error_messages = dict()

def encrypt(data):
    stringBytes = bytes(data,'UTF-8')
    encr = f.encrypt(stringBytes)
    return encr


# def index(request):
#     return render(request,'registration/index.html')

def show(request):
    print(request.method)
    if(request.method=="POST"):
        temp = myValidate.validateRequired(request.POST['height'])
        if isinstance(temp,list):
            for error in temp:
                # error_messages.setdefault('height',[]).append(error)
                error_messages.update({'height':error})

        validateRequired = myValidate.validateRequired(request.POST['name'])
        
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'name':error})
                print(error_messages)

        validateRequired = myValidate.validateRequired(request.POST['age'])
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'age':error})

        validateRequired = myValidate.validateGreaterThan0(request.POST['age'])
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'age':error})
        
        validateRequired = myValidate.validateRequired(request.POST['weight'])
        
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'weight':error})
                print(error_messages)
        

        # print(request.POST.getlist('priority'))
        validateRequired = myValidate.validateRequired(request.POST.getlist('priority'))
        
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'priority':error})
                print(error_messages)


        validateRequired = myValidate.validateRequired(request.POST.getlist('priority1'))
        
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'priority1':error})
                print(error_messages)
        

        validateRequired = myValidate.validateRequired(request.POST.getlist('priority2'))
        
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'priority2':error})
                print(error_messages)

        validateRequired = myValidate.validateRequired(request.POST.getlist('priority3[]'))
        
        if isinstance(validateRequired,list):
            for error in validateRequired:
                error_messages.update({'priority3':error})
                print(error_messages)


        name = encrypt(request.POST['name'])
        age = encrypt(request.POST['age'])
        height = request.POST['height']
        weight = request.POST['weight']
        facilities1 = request.POST.get('priority','')        
        facilities2 = request.POST.get('priority1','')
        facilities3 = request.POST.get('priority2','')

        sports = request.POST.getlist('priority3[]')

        # print(sports)
        my_string = ','.join(sports)

        print(error_messages)
        # print(my_string)
        if(len(error_messages) == 0):
            r = Register(name=name,age=age,height=height,weight=weight,facilities1=facilities1,facilities2=facilities2,facilities3=facilities3,sports=my_string)
            r.save()
    elif(request.method =="GET"):
        error_messages.clear()  

        
    return render(request,'registration/nutri-infotainment.html',{'error_messages':error_messages})

def get(request):
    list = Register.objects.all()
    for obj in list:
        obj.name = f.decrypt(obj.name).decode('UTF-8')
        obj.age = f.decrypt(obj.age).decode('UTF-8')
        
    return render(request,'registration/get.html',{'list':list})