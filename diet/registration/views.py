import io
import ast
from typing import NewType
from django.contrib.auth.models import Group
from django.db.models.expressions import F

import openpyxl
import string
import random
import xlsxwriter
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from datetime import datetime,date
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .decorators import *

from registration.models import *
from .forms import *
from shared.encryption import EncryptionHelper


def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()

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
            print(form.errors.as_data())
            return render(request,'registration_form/parents_info.html',{'form':form,'user_creation_form':user_creation_form})
    

def students_info(request):
    if request.method == "GET":
        form = StudentsInfoForm()
        user_creation_form = UserCreationForm() 
        return render(request,'registration_form/students_info.html',{'form':form,'user_creation_form':user_creation_form})
    else:        
        previousPOST = request.session['data']
        form = StudentsInfoForm(request.POST)
        studentuserform =  UserCreationForm(request.POST)
        parentform = ParentsInfoForm(previousPOST)
        parentuserform =  UserCreationForm(previousPOST)
        if form.is_valid() and studentuserform.is_valid():                        
            encryptionHelper = EncryptionHelper()
            parentUser = parentuserform.save(commit=False)
            parentUser.save()
            parent_group = Group.objects.get(name='Parents')
            parentUser.groups.add(parent_group)
            parentUser.save()

            parent = parentform.save(commit=False)    
            parent.user = parentUser
            parent.first_password = ''
            parent.password_changed = True                       
            parent.name = encryptionHelper.encrypt(previousPOST['name'])
            parent.email = encryptionHelper.encrypt(previousPOST['email'])
            parent.save()

            studentuser = studentuserform.save(commit=False)
            studentuser.save()
            student_group = Group.objects.get(name='Students')
            studentuser.groups.add(student_group)
            studentuser.save()

            student = form.save(commit=False)
            student.user = studentuser            
            student.first_password = ''
            student.password_changed = True
            student.name = encryptionHelper.encrypt(request.POST['name'])
            student.parent = parent
            student.save()


            user = authenticate(request, username=previousPOST['username'], password=previousPOST['password1'])
            if user is not None:
                login(request, user)
            
            del request.session['data']
            return redirect('/parent_dashboard')
        else:                        
            return render(request,'registration_form/students_info.html',{'form':form,'user_creation_form':studentuserform})


def loginU(request):
    if request.method == "GET":
        form = CustomAuthenticationForm()
        return render(request,'registration_form/login.html',{'form':form})
    else:
        username = request.POST['username']
        password = request.POST['password']
        grp = request.POST['groups']
        user = authenticate(request, username=username, password=password)
        grp_name = Group.objects.get(pk=grp).name
        form = CustomAuthenticationForm(request.POST)
        if user is not None:
            if is_member(user,grp):
                login(request,user)                
                if grp_name == 'Parents':
                    return redirect('/parent_dashboard')
                elif grp_name == 'Students':
                    return redirect('/student_dashboard')
                elif grp_name == 'Teachers':
                    return redirect('/teacher_dashboard')
            else:
                messages.error(request, 'User does not belong to selected group')
                return render(request,'registration_form/login.html',{'form':form})
        else:
            messages.error(request, 'Invalid credentials')
            return render(request,'registration_form/login.html',{'form':form})

@login_required(login_url='/login')
def dashboard(request):
    if request.method == "GET":
        students = ParentsInfo.objects.filter(user= request.user).first().studentsinfo_set.all()
        helper = EncryptionHelper()
        for student in students:            
            student.name = helper.decrypt(student.name)
        return render(request,'registration_form/dashboard.html',{'students':students})


@login_required(login_url='/login')
def logoutU(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')             
def addStudentForm(request):
    if request.method == "GET":
        form = StudentsInfoForm()
        user_creation_form = UserCreationForm() 
        return render(request,'registration_form/add_student.html',{'form':form,'user_creation_form':user_creation_form})
    else:
        form = StudentsInfoForm(request.POST)
        studentuserform =  UserCreationForm(request.POST)
        if form.is_valid() and studentuserform.is_valid():                        
            encryptionHelper = EncryptionHelper()
            studentuser = studentuserform.save(commit=False)
            studentuser.save()   
            student_group = Group.objects.get(name='Students')
            studentuser.groups.add(student_group)
            studentuser.save()

            student = form.save(commit=False)
            student.user = studentuser
            student.first_password = ''
            student.password_changed = True
            student.name = encryptionHelper.encrypt(request.POST['name'])            
            student.parent = ParentsInfo.objects.filter(user= request.user).first()
            student.save()
            return redirect('/parent_dashboard')
        else:                        
            return render(request,'registration_form/add_student.html',{'form':form,'user_creation_form':studentuserform})


@login_required(login_url='/login')
@user_passes_test(is_teacher,login_url='/forbidden')
def bulkRegister(request):
    if(request.method=="GET"):
        return render(request,'registration/bulkregistration.html')
    else:
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
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'F':
                    row_data.append(str(cell.value))
                elif cell.column_letter == 'G':
                    row_data.append(str(cell.value))
            student_data.append(row_data)

        
        for index,row in enumerate(parent_data):
            if index == 0:                
                continue  
            #creating parent user
            skipparent = False
            parentData = ParentsInfo.objects.all()
            for parent in parentData:                
                if encryptionHelper.decrypt(parent.email) == encryptionHelper.decrypt(row[0]):
                    skipparent = True
                    break
               
            if not skipparent:              
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))                      
                parentUser = User(username=row[2])
                parentUser.set_password(password)
                parentUser.save()
                parent_group = Group.objects.get(name='Parents')
                parentUser.groups.add(parent_group)
                parentUser.save()

                #getting data from db for foreign keys
                city = City.objects.filter(city__icontains=row[9]).first()
                state = State.objects.filter(state__icontains=row[10]).first()
                education = Education.objects.filter(education__icontains=row[11]).first()
                occupation = Occupation.objects.filter(occupation__icontains=row[12]).first()
                religion = ReligiousBelief.objects.filter(religion__icontains=row[13]).first()
                familyType = FamilyType.objects.filter(family__icontains=row[14]).first()  
                #creating parent
                parent = ParentsInfo(email=row[0],name=row[1],gender=row[3],age=row[4],address=row[5],pincode=row[6],no_of_family_members=row[7],children_count=row[8],city=city,state=state,edu=education,occupation=occupation,religion=religion,type_of_family=familyType,first_password=password)
                parent.user = parentUser                
                parent.save()
        
        
        for index,row in enumerate(student_data):
            if index == 0:
                continue  
            #creating student user
            skipstudent = StudentsInfo.objects.filter(rollno = row[3]).first()                
            if not skipstudent:               
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))
                studentUser = User(username=row[1])
                studentUser.set_password(password)
                studentUser.save()
                student_group = Group.objects.get(name='Students')
                studentUser.groups.add(student_group)
                studentUser.save()

                #getting data from db for foreign keys                
                parentData = ParentsInfo.objects.all()
                for tempparent in parentData:
                    if encryptionHelper.decrypt(tempparent.email) == row[7]:
                        parent = tempparent
                  
                school = School.objects.filter(name__icontains=row[6]).first()                
                teacher = TeacherInCharge.objects.filter(user = request.user).first()
                #creating student                 
                dob = datetime.strptime(row[5],'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                student = StudentsInfo(name=row[0],address=row[2],rollno=row[3],gender=row[4],dob=dob,school=school,first_password=password,teacher=teacher)
                student.parent = parent
                student.user = studentUser
                student.save()    
        return redirect('/bulkRegister')


@login_required(login_url='/login')
def getTemplate(request):
    output = io.BytesIO()
    
    wb =  xlsxwriter.Workbook(output)
    ws = wb.add_worksheet("Parents Data")
    ws2 = wb.add_worksheet("Students Data")
    
    columns = ["Parent Email","Parent Name","Gender","Age","Address","Pincode","No of family members","Children Count","City","State","Education","Occupation","Religion","Type of family"]
    columns2 = ["Student Name","Address","Registration No","Gender","DOB","School","Parents email"]    

    sampleParentData =["john@gmail.com","John Doe","Male","29","Mumbai","400001","5","2","Mumbai","Maharashtra","BTech","Engineer","Hindu","Nuclear"]


    sampleStudentData =["Jane Doe","Mumbai","1234","Female",date.today().strftime("%d-%m-%Y"),"K.J Somaiya School","john@gmail.com"]
    row_num = 0    

    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

    for col_num in range(len(columns2)):
        ws2.write(row_num, col_num, columns2[col_num]) # at 0 row 0 column 

    row_num+=1
    for col_num in range(len(sampleParentData)):
        ws.write(row_num, col_num, sampleParentData[col_num])

    for col_num in range(len(sampleStudentData)):
        ws2.write(row_num, col_num, sampleStudentData[col_num])
    wb.close()

    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=template.xlsx"

    return response  

@login_required(login_url='/login')
def downloadData(request):

    output = io.BytesIO()
    wb =  xlsxwriter.Workbook(output)
    parentSheet = wb.add_worksheet("Parents Data")
    studentSheet = wb.add_worksheet("Students Data")
    encryptionHelper = EncryptionHelper()

    #student sheet
    row_num = 0
    studentColumns = ['Name','Roll No','DOB','Gender','Address','School','Parent\'s Email','Username', 'Password']
    for col_num in range(len(studentColumns)):
        studentSheet.write(row_num, col_num, studentColumns[col_num]) # at 0 row 0 column 

    teacher = TeacherInCharge.objects.filter(user = request.user).first()
    rows = StudentsInfo.objects.filter(teacher=teacher).values_list('name','rollno','dob','gender','address','school','parent','user','first_password','password_changed')    
    parentEmail = []    
    for row in rows:        
        row_num += 1
        for col_num in range(len(studentColumns)):            
            if(col_num==0):                                               
                studentSheet.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]))
            
            elif(col_num==2):
                studentSheet.write(row_num, col_num, row[col_num].strftime('%d/%b/%Y'))

            elif(col_num==5):
                school = School.objects.get(pk=row[col_num])
                studentSheet.write(row_num, col_num, school.name)

            elif(col_num==6):
                parent = ParentsInfo.objects.get(pk=row[col_num])
                email = encryptionHelper.decrypt(parent.email)
                if email not in parentEmail:
                    parentEmail.append(email)
                studentSheet.write(row_num, col_num, email)

            elif(col_num==7):
                user = User.objects.get(pk=row[col_num])
                studentSheet.write(row_num, col_num, user.username)

            elif(col_num==8):
                msg = row[col_num]
                if row[col_num+1]:
                    msg = "Already Changed"
                studentSheet.write(row_num, col_num, msg)

            elif col_num==9:
                continue

            else:
                studentSheet.write(row_num, col_num, row[col_num])

    
    # Sheet header, first row
    row_num = 0
    
    #parent sheet
    parentColumns = ['Name','Email','Age','Gender','Address','City','State','Pincode','Education','Occupation','Religion','Family count','Children count','Family Type','Username','Password']
    for col_num in range(len(parentColumns)):
        parentSheet.write(row_num, col_num, parentColumns[col_num]) # at 0 row 0 column 

    rows = ParentsInfo.objects.all().values_list('name','email','age','gender','address','city','state','pincode','edu','occupation','religion','no_of_family_members','children_count','type_of_family','user','first_password','password_changed')    
    for row in rows:                
        if encryptionHelper.decrypt(row[1]) in parentEmail:
            row_num += 1
            for col_num in range(len(parentColumns)):   
                               
                if(col_num==0):              
                    parentSheet.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]))
                
                elif(col_num==1):             
                    parentSheet.write(row_num, col_num, encryptionHelper.decrypt(row[col_num]))

                elif(col_num==5):
                    city = City.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, city.city)

                elif(col_num==6):
                    state = State.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, state.state)

                elif(col_num==8):
                    education = Education.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, education.education)

                elif(col_num==9):
                    occupation = Occupation.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, occupation.occupation)

                elif(col_num==10):
                    religion = ReligiousBelief.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, religion.religion)

                elif(col_num==13):
                    familyType = FamilyType.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, familyType.family)

                elif(col_num==14):
                    user = User.objects.get(pk=row[col_num])
                    parentSheet.write(row_num, col_num, user.username)

                elif(col_num==15):
                    msg = row[col_num]
                    if row[col_num+1]:
                        msg = "Already Changed"
                    parentSheet.write(row_num, col_num, msg)

                elif col_num==16:
                    continue

                else:
                    parentSheet.write(row_num, col_num, row[col_num])

    
    wb.close()
    # construct response
    output.seek(0)
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=Parent and Student list.xlsx"
    return response


# def getFirstModule(request):
#     if(request.method == "GET"):
#         form = FirstModuleForm()
#         return render(request,'registration_form/first_module.html',{'form':form})
#     else:
#         request.session['data'] = request.POST
#         return redirect('/nutriPartTwo')


# def nutri(request):    
#     return redirect('nutriPartTwo')

# def nutriPartTwo(request):
#     if(request.method == "GET"):
#         form = FirstModuleForm()
#         return render(request,'registration_form/first_module_second.html',{'form':form})
#     else:        
#         print(','.join(request.POST.getlist('drinks')))

def student_dashboard(request):
    return render(request,'registration_form/student_dashboard.html')

def teacher_dashboard(request):
    teacher = TeacherInCharge.objects.get(user=request.user)
    total_students = teacher.studentsinfo_set.all()
    # print(students)
    result = []
    for student in total_students:
        if ModuleOne.objects.filter(student=student).exists():
            draftForm = ModuleOne.objects.get(student=student)            
            if not draftForm.draft:
                result.append(student)

    finalResult = []
        
    finalResult.append(len(result))
    finalResult.append(len(total_students)-len(result))

    return render(request,'registration_form/teacher_dashboard.html',{'result':result,'total_students':total_students,'finalResult':finalResult,'labels':['Filled','Not Filled']})

#user to check if a user belongs to a group
def is_member(user,grp):
    grp = Group.objects.get(pk=grp)
    return user.groups.filter(name=grp).exists()

# def test(request):
#     str = "DSRV"
#     school = School.objects.filter(name__icontains = str).first()



def createTempDict(postData):
    temp = {}       
    for key in postData:                            
            if key == 'source_fruits_vegetables' or key=='grow_own_food':
                temp[key] = postData.getlist(key)
            else:
                temp[key] = postData[key]
    del temp['csrfmiddlewaretoken'] 
    return temp

def creatingOrUpdatingDrafts(temp,user):
    student = StudentsInfo.objects.get(user=user)
    startdate = FormDetails.objects.get(form=Form.objects.get(name='moduleOne'),teacher=student.teacher,open=True).start_timestamp        
    if ModuleOne.objects.filter(student=student,submission_timestamp__gte=startdate).exists(): 
        draftForm = ModuleOne.objects.get(student=StudentsInfo.objects.get(user=user),submission_timestamp__gte=startdate)  
        if draftForm.draft:
        # updating drafts
            for name in ModuleOne._meta.get_fields():
                name = name.column
                if name == 'id' or name == 'student_id' or name == 'draft':
                        continue
                if name in temp:
                    setattr(draftForm, name, temp[name])      
                else:
                    setattr(draftForm, name, getattr(draftForm, name) or None) 

            draftForm.submission_timestamp = datetime.datetime.now()
            draftForm.save()
            return True
    else:
        return False

def draft(request):
    if 'parent_dashboard' in request.META.get('HTTP_REFERER').split('/'):
        module = request.META.get('HTTP_REFERER').split('/')[-1]
        id =  request.META.get('HTTP_REFERER').split('/')[-2]    
        user = StudentsInfo.objects.get(pk=id).user   
    else:
        module = request.META.get('HTTP_REFERER').split('/')[-2]  
        user = request.user  

    #1st Page
    if module=="moduleOne":         
        #for removing csrf field 
        temp = createTempDict(request.POST)  
        #checking if draft exists    
        if not creatingOrUpdatingDrafts(temp,user):
            #creating new record
            form = ModuleOne(**temp)
            form.student = StudentsInfo.objects.get(user=user)
            form.draft = True
            formType = getFormType('moduleOne')
            form.pre = 1 if formType=='PreTest' else 0
            form.submission_timestamp = datetime.datetime.now()
            form.save()
    #2nd Page
    elif module=="moduleOne-2":
        temp = createTempDict(request.POST)  
        creatingOrUpdatingDrafts(temp,user)
    #3rd Page
    elif module=="moduleOne-3":
        temp = createTempDict(request.POST)             
        creatingOrUpdatingDrafts(temp,user)
    return redirect(request.META.get('HTTP_REFERER'))
 

def getFormType(moduleType):
    module = Form.objects.get(name=moduleType)
    formType = FormDetails.objects.filter(form=module,open=True).first()
    return 'PreTest' if formType.pre else 'PostTest'


@isActive('moduleOne','student')
def moduleOne(request,user=None):
    if(request.method=="GET"):                      
        if user==None:
            user = request.user

        student = StudentsInfo.objects.get(user=user)
        startdate = FormDetails.objects.get(form=Form.objects.get(name='moduleOne'),teacher=student.teacher,open=True).start_timestamp        
        if ModuleOne.objects.filter(student=student,submission_timestamp__gte=startdate).exists(): 
            draftForm = ModuleOne.objects.get(student=StudentsInfo.objects.get(user=user),submission_timestamp__gte=startdate)            
            if draftForm.draft:
                mod = ModuleOneForm()
                temp = {}
                for name in ModuleOne._meta.get_fields():
                    name = name.column
                    if name in mod.fields:                   
                        if name == 'source_fruits_vegetables' or name=='grow_own_food':
                            temp[name] = ast.literal_eval(getattr(draftForm, name) or '[]')
                        else:
                            temp[name] = getattr(draftForm, name)
                                    
                form = ModuleOneForm(temp)   
                formPre = getFormType('moduleOne')        
                return render(request,'registration_form/module_one.html',{'form':form,'formPre':formPre})
            else:
                return redirect('/forbidden')
                        
        #new form
        else:            
            form = ModuleOneForm()
            formPre = getFormType('moduleOne')
            return render(request,'registration_form/module_one.html',{'form':form,'formPre':formPre})

    #POST            
    else:  
                
        flag = False
        if user == None:
            flag = True   
            user = request.user  
        form = ModuleOneForm(request.POST)             
        
        if form.is_valid():
            temp = createTempDict(request.POST) 

            if not creatingOrUpdatingDrafts(temp,user):
                #creating new record        
                form = ModuleOne(**temp)
                form.student = StudentsInfo.objects.get(user=user)
                form.draft = True
                formType = getFormType('moduleOne')
                form.pre = 1 if formType=='PreTest' else 0
                form.submission_timestamp = datetime.datetime.now()
                form.save()

            if flag:
                return redirect('/moduleOne-2')
            else:                
                return redirect('parentsModuleOne2',id=StudentsInfo.objects.get(user=user).id)
        
        else:            
            formPre = getFormType('moduleOne')
            return render(request,'registration_form/module_one.html',{'form':form,'formPre':formPre})    

        


def moduleOne2(request,user=None):
    if(request.method=="GET"):
        if user==None:
            user = request.user
            
        student = StudentsInfo.objects.get(user=user)
        startdate = FormDetails.objects.get(form=Form.objects.get(name='moduleOne'),teacher=student.teacher,open=True).start_timestamp        
        if ModuleOne.objects.filter(student=student,submission_timestamp__gte=startdate).exists(): 
            draftForm = ModuleOne.objects.get(student=StudentsInfo.objects.get(user=user),submission_timestamp__gte=startdate)            
            if draftForm.draft:
                mod = ModuleOneForm2()
                temp = {}
                for name in ModuleOne._meta.get_fields():
                    name = name.column
                    if name in mod.fields:  
                        temp[name] = getattr(draftForm, name) or None
        
                form = ModuleOneForm2(temp)                           
                formPre = getFormType('moduleOne')
                print(formPre)
                return render(request,'registration_form/module_one2.html',{'form':form,'formPre':formPre})
          
        #new form
        else:            
            form = ModuleOneForm2()
            formPre = getFormType('moduleOne')
            # print(formPre)
            return render(request,'registration_form/module_one2.html',{'form':form,'formPre':formPre})
    #POST
    else:
        flag = False
        if user == None:
            flag = True   
            user = request.user 
        form = ModuleOneForm2(request.POST)                

        if form.is_valid():
            temp = createTempDict(request.POST)             
            creatingOrUpdatingDrafts(temp,user)

            if flag:
                return redirect('/moduleOne-3')
            else:                
                return redirect('parentsModuleOne3',id=StudentsInfo.objects.get(user=user).id)                    
        else:
            formPre = getFormType('moduleOne')
            return render(request,'registration_form/module_one2.html',{'form':form,'formPre':'formPre'})
            

def moduleOne3(request,user=None):
    if(request.method=="GET"):
        if user==None:
            user = request.user

        student = StudentsInfo.objects.get(user=user)
        startdate = FormDetails.objects.get(form=Form.objects.get(name='moduleOne'),teacher=student.teacher,open=True).start_timestamp        
        if ModuleOne.objects.filter(student=student,submission_timestamp__gte=startdate).exists(): 
            draftForm = ModuleOne.objects.get(student=StudentsInfo.objects.get(user=user),submission_timestamp__gte=startdate)            
            if draftForm.draft:
                mod = ModuleOneForm3()
                temp = {}
                for name in ModuleOne._meta.get_fields():
                    name = name.column
                    if name in mod.fields:                  
                        temp[name] = getattr(draftForm, name) or None
                form = ModuleOneForm3(temp)                           
                formPre = getFormType('moduleOne')
                return render(request,'registration_form/module_one3.html',{'form':form,'formPre':formPre})
            else:
                return redirect('/404notFound')            
        #new form
        else:            
            form = ModuleOneForm3()
            formPre = getFormType('moduleOne')
            return render(request,'registration_form/module_one3.html',{'form':form,'formPre':formPre})
    #POST
    else:
        flag = False
        if user == None:
            flag = True   
            user = request.user
        form = ModuleOneForm3(request.POST)                
            
        #valid form
        if form.is_valid():                    
            temp = createTempDict(request.POST)
            student = StudentsInfo.objects.get(user=user)
            startdate = FormDetails.objects.get(form=Form.objects.get(name='moduleOne'),teacher=student.teacher,open=True).start_timestamp        
            draftForm = ModuleOne.objects.get(student=StudentsInfo.objects.get(user=user),submission_timestamp__gte=startdate)
            if draftForm.draft:
                for name in ModuleOne._meta.get_fields():
                    name = name.column
                    if name == 'id' or name == 'student_id' or name == 'draft':
                            continue                    
                    elif name == 'source_fruits_vegetables' or name == 'grow_own_food':
                        list = '; '.join(ast.literal_eval(getattr(draftForm, name)))
                        setattr(draftForm, name, list)      
                    elif name in temp:
                        setattr(draftForm, name, temp[name])      

                draftForm.draft = False
                draftForm.submission_timestamp = datetime.datetime.now()
                draftForm.save()
                if flag:
                    return redirect('/student_dashboard')
                else:
                    return redirect('/parent_dashboard')            
        #invalid form
        else:                               
            formPre = getFormType('moduleOne')
            return render(request,'registration_form/module_one3.html',{'form':form,'formPre':formPre})
            

def forbidden(request):
    raise PermissionDenied

def showStudent(request,id):
    student = StudentsInfo.objects.get(pk=id)
    encryptionHelper = EncryptionHelper()
    return render(request,'registration_form/student_modules.html')

@isActive('moduleOne','parent')
def parentModuleOne(request,id):
    user = StudentsInfo.objects.get(pk=id).user
    return moduleOne(request,user)

def parentModuleOne2(request,id):
    user = StudentsInfo.objects.get(pk=id).user
    return moduleOne2(request,user)
  

def parentModuleOne3(request,id):
    user = StudentsInfo.objects.get(pk=id).user
    return moduleOne3(request,user)



def previous(request):
    link = request.META.get('HTTP_REFERER').split('/')
    print(link)
    if 'parent_dashboard' in link:
        if link[-1] == 'moduleOne-2':
            link[-1] = 'moduleOne'
        elif link[-1] == 'moduleOne-3':
            link[-1] = 'moduleOne-2' 
    else:
        if link[-2] == 'moduleOne-2':
            link[-2] = 'moduleOne'
        elif link[-2] == 'moduleOne-3':
            link[-2] = 'moduleOne-2' 
    newLink = '/'.join(link)
    print(newLink)
    return redirect(newLink)

def unmatched(request):
    return HttpResponse("<h1>404 Page Not Found</h1>")
    
def manageForms(request):
    if request.method == "GET":
        moduleOne={}
        moduleTwo={}
        moduleThree={}
        form = Form.objects.get(name='moduleOne')
        teacher = TeacherInCharge.objects.get(user=request.user)
        if FormDetails.objects.filter(form=form,teacher=teacher).exists():

            form = FormDetails.objects.filter(form=form,teacher=teacher,open=True).order_by('-start_timestamp').first()            
            if form:
                if form.pre:
                    moduleOne['pre'] = True
                    moduleOne['post'] = False

                else:
                    moduleOne['post'] = True
                    moduleOne['pre'] = False

        return render(request,'registration_form/manage_forms_teacher.html',{'moduleOne': moduleOne, 'moduleTwo':moduleTwo, 'moduleThree':moduleThree})
    else:
        
        if 'moduleOne' in request.POST:
            module_one_pre = request.POST.get('module_one_pre', False)
            module_one_post = request.POST.get('module_one_post', False)            
            if module_one_pre == 'on' and module_one_post == 'on':                
                messages.error(request, 'Cannot select both PreTest and PostTest')

            form = Form.objects.get(name='moduleOne')
            teacher = TeacherInCharge.objects.get(user=request.user)

            if module_one_pre=='on':
                if not FormDetails.objects.filter(form=form,teacher=teacher,pre=True,open=True).exists():
                    update = FormDetails(form=form,teacher=teacher,pre=True,open=True,start_timestamp=datetime.datetime.now())
                    update.save()
            else:                
                if FormDetails.objects.filter(form=form,teacher=teacher,pre=True,open=True).exists():                    
                    update = FormDetails.objects.filter(form=form,teacher=teacher,pre=True,open=True).first()                    
                    update.open = False
                    update.end_timestamp = datetime.datetime.now()
                    update.save()

            if module_one_post=='on':
                if not FormDetails.objects.filter(form=form,teacher=teacher,pre=False,open=True).exists():
                    update = FormDetails(form=form,teacher=teacher,pre=False,open=True,start_timestamp=datetime.datetime.now())
                    update.save()
            else:                            
                if FormDetails.objects.filter(form=form,teacher=teacher,pre=False,open=True).exists():                    
                    update = FormDetails.objects.filter(form=form,teacher=teacher,pre=False,open=True).first()                    
                    update.open = False
                    update.end_timestamp = datetime.datetime.now()
                    update.save()

        
        module_two_pre = request.POST.get('module_two_pre', False)
        module_two_post = request.POST.get('module_two_post', False)
        module_three_pre = request.POST.get('module_three_pre', False)
        module_three_post = request.POST.get('module_three_post', False)
            
        # if module_one_pre == module_one_post or module_two_pre == module_two_post or module_three_pre == module_three_post:
            
        
        # FormDetails.objects.filter(form= )

        return redirect('/manage-forms')
        