import io
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate
from django.core import serializers
import environ
from cryptography.fernet import Fernet
import json
from openpyxl.descriptors.base import DateTime
import xlwt
import openpyxl
import string
import random
import datetime
import xlsxwriter


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
    if(request.method=="GET"):
        return render(request,'registration/bulkregistration.html')
    else:
        print(request.POST)
        print(request.FILES)
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        parentSheet = wb["Parents Data"]
        studentSheet = wb["Students Data"]

        encryptionHelper = EncryptionHelper()

        parent_data = list()
        # iterating over the rows and
        # getting value from each cell in row        
        for row in parentSheet.iter_rows():
            row_data = list()
            for cell in row:                                
                if cell.row == 1 :                
                    continue
                if cell.column_letter == 'A':                    
                    row_data.append(encryptionHelper.encrypt(str(cell.value)))
                elif cell.column_letter == 'B':
                    row_data.append(encryptionHelper.encrypt(str(cell.value)))
                    row_data.append(str(cell.value.lower().replace(" ",""))+str(random.randint(11,99)))
                elif cell.column_letter == 'C':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'D':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'E':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'F':
                    row_data.append(int(cell.value))
                elif cell.column_letter == 'G':
                    row_data.append(int(cell.value))
                elif cell.column_letter == 'H':
                    row_data.append(int(cell.value))
                elif cell.column_letter == 'I':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'J':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'K':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'L':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'M':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'N':
                    row_data.append(str(cell.value))
            parent_data.append(row_data)

        student_data = list()
        # iterating over the rows and
        # getting value from each cell in row        
        for row in studentSheet.iter_rows():
            row_data = list()
            for cell in row:                                
                if cell.row == 1 :                
                    continue
                if cell.column_letter == 'A':
                    row_data.append(encryptionHelper.encrypt(str(cell.value)))
                    row_data.append(str(cell.value.lower().replace(" ",""))+str(random.randint(11,99)))
                elif cell.column_letter == 'B':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'C':
                    row_data.append(int(cell.value))
                elif cell.column_letter == 'D':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'E':
                    row_data.append(cell.value)
                elif cell.column_letter == 'F':
                    row_data.append(str(cell.value))
            student_data.append(row_data)

        parentList = []
        for index,row in enumerate(parent_data):
            if index == 0:
                parentList.append(0)
                continue  
            #creating parent user
            password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))                      
            parentUser = User(username=row[2])
            parentUser.set_password(password)
            parentUser.save()

            #getting data from db for foreign keys
            city = City.objects.filter(city=row[9].lower()).first()
            state = State.objects.filter(state=row[10].lower()).first()
            education = Education.objects.filter(education=row[11].lower()).first()
            occupation = Occupation.objects.filter(occupation=row[12].lower()).first()
            religion = ReligiousBelief.objects.filter(religion=row[13].lower()).first()
            familyType = FamilyType.objects.filter(family=row[14].lower()).first()  
            #creating parent
            parent = ParentsInfo(email=row[0],name=row[1],gender=row[3],age=row[4],address=row[5],pincode=row[6],no_of_family_members=row[7],children_count=row[8],city=city,state=state,edu=education,occupation=occupation,religion=religion,type_of_family=familyType,first_password=password)
            parent.user = parentUser
            parentList.append(parent)
            parent.save()
        
        for index,row in enumerate(student_data):
            if index == 0:
                continue  
            #creating student user
            password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
            studentUser = User(username=row[1])
            studentUser.set_password(password)
            studentUser.save()

            #getting data from db for foreign keys

            parent = parentList[index]
            school = School.objects.filter(name=row[6]).first()

            #creating student
            student = StudentsInfo(name=row[0],address=row[2],rollno=row[3],gender=row[4],dob=row[5],school=school,first_password=password)
            student.parent = parent
            student.user = studentUser
            student.save()
        
            
            
        return redirect('/bulkRegister')


def getTemplate(request):

    output = io.BytesIO()

    wb =  xlsxwriter.Workbook(output)
    ws = wb.add_worksheet("Parents Data")
    ws2 = wb.add_worksheet("Students Data")
    
    columns = ["Parent Email","Parent Name","Gender","Age","Address","Pincode","No of family members","Children Count","City","State","Education","Occupation","Religion","Type of family"]
    columns2 = ["Student Name","Address","Registration No","Gender","DOB","School"]    

    row_num = 0    

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

    for col_num in range(len(columns2)):
        ws2.write(row_num, col_num, columns2[col_num]) # at 0 row 0 column 
    wb.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=test.xlsx"

    return response  


def downloadData(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xlsx"'

    wb = xlwt.Workbook(encoding='utf-8')
    parentSheet = wb.active_sheet
    parentSheet.title = "Parents Data"
    studentSheet = wb.add_sheet('Students Data') 

    # Sheet header, first row
    # row_num = 0

    # encryptionHelper = EncryptionHelper()


    # #parent sheet
    # parentColumns = ['Name','Email','Age','Gender','Address','City','State','Pincode','Education','Occupation','Religion','Family count','Children count','Family Type','Username','Password']

    # parentSheet.append(parentColumns)

    # for col_num in range(len(parentColumns)):
    #     parentSheet.write(row_num, col_num, parentColumns[col_num], font_style) # at 0 row 0 column 

    # rows = ParentsInfo.objects.all().values_list('name','email','age','gender','address','city','state','pincode','edu','occupation','religion','no_of_family_members','children_count','type_of_family','user','first_password','password_changed')

    # for row in rows:        
    #     row_num += 1
    #     for col_num in range(len(parentColumns)):            
    #         if(col_num==0):  
    #             print(encryptionHelper.decrypt(row[col_num]))              
    #             parentSheet.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]), font_style)
            
    #         elif(col_num==1):
    #             print(encryptionHelper.decrypt(row[col_num]))              
    #             parentSheet.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]), font_style)

    #         elif(col_num==5):
    #             city = City.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, city.city, font_style)

    #         elif(col_num==6):
    #             state = State.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, state.state, font_style)

    #         elif(col_num==8):
    #             education = Education.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, education.education, font_style)

    #         elif(col_num==9):
    #             occupation = Occupation.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, occupation.occupation, font_style)

    #         elif(col_num==10):
    #             religion = ReligiousBelief.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, religion.religion, font_style)

    #         elif(col_num==13):
    #             familyType = FamilyType.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, familyType.family, font_style)

    #         elif(col_num==14):
    #             user = User.objects.get(pk=row[col_num])
    #             parentSheet.write(row_num, col_num, user.username, font_style)

    #         elif(col_num==15):
    #             msg = row[col_num]
    #             if row[col_num+1]:
    #                 msg = "Already Changed"
    #             parentSheet.write(row_num, col_num, msg, font_style)

    #         elif col_num==16:
    #             continue

    #         else:
    #             print(row[col_num])
    #             parentSheet.write(row_num, col_num, row[col_num], font_style)


    # #student sheet
    # studentColumns = ['Name','Roll No','DOB','Gender','Address','School','Parent\'s Email','Username', 'Password']

    # for col_num in range(len(studentColumns)):
    #     studentSheet.write(row_num, col_num, studentColumns[col_num], font_style) # at 0 row 0 column 

    
    # rows = StudentsInfo.objects.all().values_list('name','rollno','dob','gender','address','school','parent','user','first_password','password_changed')    

    # for row in rows:        
    #     row_num += 1
    #     for col_num in range(len(studentColumns)):            
    #         if(col_num==0):  
    #             print(encryptionHelper.decrypt(row[col_num]))              
    #             studentSheet.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]), font_style)
            
    #         elif(col_num==2):
    #             print(row[col_num].strftime('%d/%b/%Y'))
    #             studentSheet.write(row_num, col_num, row[col_num].strftime('%d/%b/%Y'), font_style)

    #         elif(col_num==5):
    #             school = School.objects.get(pk=row[col_num])
    #             studentSheet.write(row_num, col_num, school.name, font_style)

    #         elif(col_num==6):
    #             parent = ParentsInfo.objects.get(pk=row[col_num])
    #             studentSheet.write(row_num, col_num, encryptionHelper.decrypt(parent.email), font_style)

    #         elif(col_num==7):
    #             user = User.objects.get(pk=row[col_num])
    #             print(user.username)
    #             studentSheet.write(row_num, col_num, user.username, font_style)

    #         elif(col_num==8):
    #             msg = row[col_num]
    #             if row[col_num+1]:
    #                 msg = "Already Changed"
    #             studentSheet.write(row_num, col_num, msg, font_style)

    #         elif col_num==9:
    #             continue

    #         else:
    #             print(row[col_num])
    #             studentSheet.write(row_num, col_num, row[col_num], font_style)
    
    wb.save('students.xlsx')
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