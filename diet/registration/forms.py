from django.forms import ModelForm
from django import forms
from .models import ParentsInfo, StudentsInfo

class ConsentForm(forms.Form):
    consent = forms.BooleanField(
        error_messages={'required': 'You must agree to consent form'},
        label="I Agree"
        )
            
class ParentsInfoForm(ModelForm):
    class Meta:
        model = ParentsInfo
        fields = ['name','email','gender','age','occupation','state','city','edu','address','pincode','no_of_family_members','type_of_family','religion','children_count']
        labels = {
            'edu': 'Education',
        }

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
        fields = ['name','school','gender','rollno','dob','address']
        
    GENDER_CHOICES=[('Male','Male'),
         ('Female','Female'),
         ('Other','Other')]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    
    address= forms.CharField(max_length=100,widget= forms.Textarea())

    
    def clean(self):
        super(StudentsInfoForm, self).clean()

        name = self.cleaned_data.get('name')
        # print(name)
        if not name:
            self.add_error('name','Name is a required Field')
        
        return self.cleaned_data
