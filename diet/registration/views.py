from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate
from django.core import serializers
import environ
from cryptography.fernet import Fernet
import json
import xlwt
import openpyxl
import string
import random
import datetime


from registration.models import *
from .forms import ConsentForm,ParentsInfoForm, StudentsInfoForm
from shared.encryption import EncryptionHelper

# env = environ.Env()
# environ.Env.read_env()
# key: bytes = bytes(env('KEY'),'ascii')
# f = Fernet(key)

# error_messages = dict()

# def encrypt(data):
#     stringBytes = bytes(data,'UTF-8')
#     encr = f.encrypt(stringBytes)
#     return encr



def home(request):
    return render(request, "registration_form/home.html")

def consent(request):
    if request.method == "GET":
        form = ConsentForm()
        return render(request,'registration_form/consent.html',{'form':form})

def parents_info(request):
    if request.method == "GET":
        if(request.session.get('data')):
            form = ParentsInfoForm(request.session.get('data'))
            user_creation_form = UserCreationForm(request.session.get('data'))
        else:
            form = ParentsInfoForm()
            user_creation_form = UserCreationForm() 
        return render(request,'registration_form/parents_info.html',{'form':form,'user_creation_form':user_creation_form})
    else:
        form = ParentsInfoForm(request.POST)
        user_creation_form =  UserCreationForm(request.POST)

        if form.is_valid() and user_creation_form.is_valid():            
            request.session['data'] = request.POST
            return redirect('/students_info')
        else:            
            print(form.errors.as_data() )
            return render(request,'registration_form/parents_info.html',{'form':form,'user_creation_form':user_creation_form})
    

def students_info(request):
    if request.method == "GET":
        form = StudentsInfoForm()
        user_creation_form = UserCreationForm() 
        return render(request,'registration_form/students_info.html',{'form':form,'user_creation_form':user_creation_form})
    else:        
        previousPOST = request.session.get('data')
        form = StudentsInfoForm(request.POST)
        studentuserform =  UserCreationForm(request.POST)
        parentform = ParentsInfoForm(previousPOST)
        parentuserform =  UserCreationForm(previousPOST)
        if form.is_valid() and studentuserform.is_valid():                        
            encryptionHelper = EncryptionHelper()
            parentUser = parentuserform.save(commit=False)
            parentUser.save()
            parent = parentform.save(commit=False)   
            parent.user = parentUser
            # print(request.session.get('data'))
            # print(parent.name)
            # print(type(parent.name))
            parent.name = encryptionHelper.encrypt(previousPOST['name'])
            print(encryptionHelper.decrypt(parent.name))
            parent.email = encryptionHelper.encrypt(previousPOST['email'])
            print(encryptionHelper.decrypt(parent.email))
            parent.save()


            studentuser = studentuserform.save(commit=False)
            studentuser.save()   
            student = form.save(commit=False)
            student.user = studentuser
            student.name = encryptionHelper.encrypt(request.POST['name'])
            print(encryptionHelper.decrypt(student.name))
            student.parent = parent
            student.save()
            
            return redirect('/home')
        else:            
            print(form.errors.as_data())
            return render(request,'registration_form/students_info.html',{'form':form,'user_creation_form':studentuserform})


def parent_login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request,'registration_form/parent_login.html',{'form':form})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        form = AuthenticationForm(request.POST)
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request,'registration_form/parent_login.html',{'form':form})

def bulkRegister(request):
    return render(request,'registration/bulkregistration.html')


def getTemplate(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Parents Data') # this will make a sheet named Users Data
    ws2 = wb.add_sheet('Students Data')
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ["Parent Email","Parent Name","Gender","Age","Address","Pincode","No of family members","Children Count","City","Education","Occupation","Religion","State","Type of family"]
    columns2 = ["Student Name","Address","Registration No","Gender","DOB","School"]    

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    for col_num in range(len(columns2)):
        ws2.write(row_num, col_num, columns2[col_num], font_style) # at 0 row 0 column 

    wb.save(response)
    return response  


def downloadData(request):
    print('hereee')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Student\'s Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name','Roll No','DOB','Gender','Address','School','Parent\'s Name','Username', 'Password']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()    
    encryptionHelper = EncryptionHelper()
    
    rows = StudentsInfo.objects.all().values_list('name','rollno','dob','gender','address','school','parent','user','user')    

    for row in rows:        
        row_num += 1
        for col_num in range(len(columns)):            
            if(col_num==0):  
                print(encryptionHelper.decrypt(row[col_num]))              
                ws.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]), font_style)
            
            elif(col_num==2):
                print(row[col_num].strftime('%d/%b/%Y'))
                ws.write(row_num, col_num, row[col_num].strftime('%d/%b/%Y'), font_style)

            elif(col_num==5):
                school = School.objects.get(pk=row[col_num])
                print(school.name)
                ws.write(row_num, col_num, school.name, font_style)

            elif(col_num==6):
                parent = ParentsInfo.objects.get(pk=row[col_num])
                print(encryptionHelper.decrypt(parent.name))                                
                ws.write(row_num, col_num, encryptionHelper.decrypt(parent.name), font_style)

            elif(col_num==7):
                user = User.objects.get(pk=row[col_num])
                print(user.username)
                ws.write(row_num, col_num, user.username, font_style)

            elif(col_num==8):
                user = User.objects.get(pk=row[col_num])
                print(user.password)
                ws.write(row_num, col_num, user.password, font_style)
            
            else:
                print(row[col_num])
                ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response


                
      

# def getExcel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="users.xls"'

#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Name','Username', 'Password', 'Age', 'Height', 'Weight']

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()

#     rows = Register.objects.all().values_list('name', 'username', 'password', 'age', 'height', 'weight', 'password_changed')
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):            
#             if(col_num==0):
#                 ws.write(row_num, col_num, f.decrypt(row[col_num]).decode('UTF-8'), font_style)

#             elif(col_num==2):
#                 if not row[6]:
#                     ws.write(row_num, col_num, row[col_num], font_style)
#                 else:
#                     ws.write(row_num, col_num, "Password Changed", font_style)

#             elif(col_num==6):
#                 continue

#             elif(col_num==3):
#                 ws.write(row_num, col_num, f.decrypt(row[col_num]).decode('UTF-8'), font_style) 

#             else:
#                 ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response

# def excelRegister(request):
#     if(request.method=="GET"):
#         return render(request,'registration/excelregister.html')
        
#     else:
#         excel_file = request.FILES["excel_file"]

#         # you may put validations here to check extension or file size

#         wb = openpyxl.load_workbook(excel_file)

#         # getting a particular sheet by name out of many sheets
#         worksheet = wb["Sheet1"]

#         excel_data = list()
#         # iterating over the rows and
#         # getting value from each cell in row        
#         for row in worksheet.iter_rows():         
#             row_data = list()
#             for cell in row:                                
#                 if cell.row == 1 :                
#                     continue
#                 if cell.column_letter == 'A':                    
#                     row_data.append(encrypt(str(cell.value)))
#                     row_data.append(str(cell.value.lower().replace(" ",""))+str(random.randint(11,99)))
#                     print('HERE')
#                 elif cell.column_letter == 'B':
#                     row_data.append(encrypt(str(cell.value)))
#                 elif cell.column_letter == 'C':
#                     row_data.append(int(cell.value))
#                 elif cell.column_letter == 'D':
#                     row_data.append(int(cell.value))
#                 elif cell.column_letter == 'E':
#                     row_data.append(str(cell.value))
#                 elif cell.column_letter == 'F':
#                     row_data.append(str(cell.value))
#                 elif cell.column_letter == 'G':
#                     row_data.append(str(cell.value))
#                 else:
#                     row_data.append(str(cell.value))
#             excel_data.append(row_data)

#         for index,row in enumerate(excel_data):
#             if index == 0:
#                 continue  
#             password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6))                      
#             print(row)
#             r = Register(name=row[0], username=row[1], age=row[2], height=int(row[3]), weight=int(row[4]), facilities1=row[5], facilities2=row[6], facilities3=row[7], sports=row[8], password=password, password_changed=False)
#             r.save()
            
#         return redirect(get)

# def show(request):    
#     if(request.method=="POST"):
#         temp = myValidate.validateRequired(request.POST['height'])
#         if isinstance(temp,list):
#             for error in temp:
#                 # error_messages.setdefault('height',[]).append(error)
#                 error_messages.update({'height':error})

#         validateRequired = myValidate.validateRequired(request.POST['name'])
        
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'name':error})
#                 print(error_messages)

#         validateRequired = myValidate.validateRequired(request.POST['age'])
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'age':error})

#         validateRequired = myValidate.validateGreaterThan0(request.POST['age'])
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'age':error})
        
#         validateRequired = myValidate.validateRequired(request.POST['weight'])
        
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'weight':error})
#                 print(error_messages)
        

#         # print(request.POST.getlist('priority'))
#         validateRequired = myValidate.validateRequired(request.POST.getlist('priority'))
        
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'priority':error})
#                 print(error_messages)


#         validateRequired = myValidate.validateRequired(request.POST.getlist('priority1'))
        
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'priority1':error})
#                 print(error_messages)
        

#         validateRequired = myValidate.validateRequired(request.POST.getlist('priority2'))
        
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'priority2':error})
#                 print(error_messages)

#         validateRequired = myValidate.validateRequired(request.POST.getlist('priority3[]'))
        
#         if isinstance(validateRequired,list):
#             for error in validateRequired:
#                 error_messages.update({'priority3':error})
#                 print(error_messages)


#         name = encrypt(request.POST['name'])
#         age = encrypt(request.POST['age'])
#         height = request.POST['height']
#         weight = request.POST['weight']
#         facilities1 = request.POST.get('priority','')        
#         facilities2 = request.POST.get('priority1','')
#         facilities3 = request.POST.get('priority2','')

#         sports = request.POST.getlist('priority3[]')
#         username = str(request.POST['name'].lower().replace(" ",""))+str(random.randint(11,99))
#         password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6))
#         # print(sports)
#         my_string = ','.join(sports)

#         print(error_messages)
#         # print(my_string)
#         if(len(error_messages) == 0):
#             r = Register(name=name,age=age,height=height,weight=weight,facilities1=facilities1,facilities2=facilities2,facilities3=facilities3,sports=my_string,username=username,password=password,password_changed=False)
#             r.save()
#     elif(request.method =="GET"):
#         error_messages.clear()  

        
#     return render(request,'registration/nutri-infotainment.html',{'error_messages':error_messages})

# def get(request):
#     list = Register.objects.all()
#     for obj in list:
#         obj.name = f.decrypt(obj.name).decode('UTF-8')
#         obj.age = f.decrypt(obj.age).decode('UTF-8')
        
#     return render(request,'registration/get.html',{'list':list})