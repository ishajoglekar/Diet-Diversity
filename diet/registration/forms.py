from django.contrib.auth.models import Group
from django.forms import ModelForm, fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_datepicker_plus import DatePickerInput
import datetime

from .models import ParentsInfo, StudentsInfo

class ConsentForm(forms.Form):
    consent = forms.BooleanField(
        error_messages={'required': 'You must agree to consent form'},
        label="I Agree"
        )
            
class ParentsInfoForm(ModelForm):
    class Meta:
        model = ParentsInfo
        fields = ['age','occupation','state','city','edu','pincode','no_of_family_members','type_of_family','religion','children_count']
        labels = {
            'edu': 'Education',
        }

    email = forms.EmailField()
    name = forms.CharField()
    GENDER_CHOICES=[('Male','Male'),
         ('Female','Female'),
         ('Other','Other')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    
    address= forms.CharField(max_length=100,widget= forms.Textarea())

    def clean(self):
        super(ParentsInfoForm, self).clean()

        name = self.cleaned_data.get('name')
        # print(name)
        if not name:
            self.add_error('name','Name is a required Field')
        
        return self.cleaned_data

class StudentsInfoForm(ModelForm):
    class Meta:
        model = StudentsInfo
        fields = ['school','gender','rollno','dob','address','teacher']
        
    labels = {
            'dob': 'Date Of Birth',
            'teacher': 'Teacher InCharge',
        }
    name = forms.CharField() 
      
    GENDER_CHOICES=[('Male','Male'),
         ('Female','Female'),
         ('Other','Other')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    
    address= forms.CharField(max_length=255,widget= forms.Textarea())
    dt = datetime.datetime.now()
    dt = dt.replace(year=dt.year-5) 
    print(dt.strftime("%m/%d/%Y"))
    widgets = {
            'start_date': DatePickerInput(), # python date-time format
            'end_date': dt.strftime("%m/%d/%Y"),
        }

    
    dob = forms.DateField(
        widget=DatePickerInput(widgets)
    )
    
    def clean(self):
        super(StudentsInfoForm, self).clean()

        name = self.cleaned_data.get('name')
        # print(name)
        if not name:
            self.add_error('name','Name is a required Field')
        
        return self.cleaned_data




class CustomAuthenticationForm(AuthenticationForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        fields = '__all__'