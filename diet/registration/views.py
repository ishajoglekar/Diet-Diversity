import io
from django.contrib.auth.models import Group
from django.http.response import HttpResponseForbidden
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


from registration.models import *
from .forms import ConsentForm,ParentsInfoForm, StudentsInfoForm,CustomAuthenticationForm,FirstModuleForm
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

            print(request.session.get('data')) 
            del request.session['data']
            return redirect('/home')
        else:            
            print(form.errors.as_data())
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
                print(grp_name)
                if grp_name == 'Parents':
                    return redirect('/parent_dashboard')
                elif grp_name == 'Students':
                    return redirect('/student_dashboard')
                elif grp_name == 'Teachers':
                    return redirect('/teacher_dashboard')
            else:
                messages.error(request, 'User does not belong to select group')
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
            print(helper.decrypt(student.name))
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
            print(encryptionHelper.decrypt(student.name))
            student.parent = ParentsInfo.objects.filter(user= request.user).first()
            student.save()
            return redirect('/parent_dashboard')
        else:            
            print(form.errors.as_data())
            return render(request,'registration_form/add_student.html',{'form':form,'user_creation_form':studentuserform})


@login_required(login_url='/login')
@user_passes_test(is_teacher)
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
        print(studentSheet.max_row)              
        for row in studentSheet.iter_rows():
            row_data = list()
            for cell in row:                                
                if cell.row == 1 :                
                    continue
                if cell.column_letter == 'A':
                    print(cell.value)
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

            print(skipparent)       
            if not skipparent:              
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 8))                      
                parentUser = User(username=row[2])
                parentUser.set_password(password)
                parentUser.save()
                parent_group = Group.objects.get(name='Parents')
                parentUser.groups.add(parent_group)
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
                parent.save()
        
        
        for index,row in enumerate(student_data):
            if index == 0:
                continue  
            #creating student user
            skipstudent = StudentsInfo.objects.filter(rollno = row[3]).first()  
            print(skipstudent)       
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
                  
                school = School.objects.filter(name=row[6].lower()).first()                
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


    sampleStudentData =["Jane Doe","Mumbai","1234","Female",date.today().strftime("%d/%m/%Y"),"K.J Somaiya School","john@gmail.com"]
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
    print("Students")
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
    print("Parents")
    for row in rows:            
        print(parentEmail)
        print(encryptionHelper.decrypt(row[1]))
        print(encryptionHelper.decrypt(row[1]) in parentEmail)
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


def getFirstModule(request):
    if(request.method == "GET"):
        form = FirstModuleForm()
        return render(request,'registration_form/first_module.html',{'form':form})
    else:
        request.session['data'] = request.POST
        return redirect('/nutriPartTwo')


def nutri(request):
    # return render(request,'registration/nutri-infotainment.html')
    return redirect('nutriPartTwo')

def nutriPartTwo(request):
    if(request.method == "GET"):
        form = FirstModuleForm()
        return render(request,'registration_form/first_module_second.html',{'form':form})
    else:
        # print(request.POST.getlist('drinks'))
        print(','.join(request.POST.getlist('drinks')))

def student_dashboard(request):
    return render(request,'registration_form/student_dashboard.html')

def teacher_dashboard(request):
    return render(request,'registration_form/teacher_dashboard.html')



#user to check if a user belongs to a group
def is_member(user,grp):
    grp = Group.objects.get(pk=grp)
    return user.groups.filter(name=grp).exists()

