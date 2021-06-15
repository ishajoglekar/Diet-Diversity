from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models.fields import CharField
from django.forms import ModelForm, fields
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from bootstrap_datepicker_plus import DatePickerInput
import datetime

from .models import ParentsInfo, StudentsInfo, ModuleOne,FirstModule

class ConsentForm(forms.Form):
    consent = forms.BooleanField(
        error_messages={'required': 'You must agree to consent form'},
        label="I Agree"
        )
            
class ParentsInfoForm(ModelForm):
    class Meta:
        model = ParentsInfo
        fields = ['age','occupation','state','city','edu','pincode','no_of_family_members','type_of_family','religion','children_count','gender','address']
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

class FirstModuleForm(ModelForm):
    class Meta:
        model = FirstModule
        fields = ['name','cricket','chess','tennis']

    labels = {
            'cricket': 'Cricket',
            'chess': 'Chess',
            'tennis': 'Tennis',
            'email' : 'Email'
        }
    name = forms.CharField() 
    email = forms.CharField() 
    PRIORITY_CHOICES=[('Daily',''),
         ('Once',''),
         ('Twice','')]

    cricket = forms.ChoiceField(choices=PRIORITY_CHOICES, widget= forms.RadioSelect(attrs={'class':'flex-item'}))
    chess = forms.ChoiceField(choices=PRIORITY_CHOICES, widget= forms.RadioSelect(attrs={'class':'flex-item'}))
    tennis = forms.ChoiceField(choices=PRIORITY_CHOICES, widget= forms.RadioSelect(attrs={'class':'flex-item'}))

    FOOD_INTAKES=[('1-5',''),
         ('6-10',''),
         ('10-15',''),
         ('>15',''),
         ('1 teaspoon',''),
         ('1 tablespoon',''),
         ('Never','')]

    food = forms.MultipleChoiceField(choices=FOOD_INTAKES, widget= forms.CheckboxSelectMultiple(attrs={'class':'flex-item'}))

    DRINKS_INTAKE=[('Water',''),
         ('Soft Drinks',''),
         ('Fruit Juices',''),
         ('Energy Drinks',''),
         ('No Drinks',''),]

    drinks = forms.MultipleChoiceField(choices=DRINKS_INTAKE, widget= forms.CheckboxSelectMultiple(attrs={'class':'flex-item'}))


class CustomAuthenticationForm(AuthenticationForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all())
    class Meta:
        fields = '__all__'



class ModuleOneForm(forms.ModelForm):
    class Meta:
        model = ModuleOne
        fields = ['nutriGarden', 'source_fruits_vegetables', 'grow_own_food', 'if_grow_what', 'reason_gardening', 'healthy_diet', 'imp_nutrients']

    if_grow_what = forms.CharField(label=("If you grow your own food, what do you grow? ( if you don't grow your own food,please specify N/A)"),max_length=255,required=False)
    FOOD_INTAKES=[('1-5',''),
         ('6-10',''),
         ('10-15',''),
         ('>15',''),
         ('1 teaspoon',''),
         ('1 tablespoon',''),
         ('Never','')]
         
    YES_NO=[('Yes','Yes'),('No','No')]

    source_fruits_vegetables_choices = [
        ('Vendor on the cart','Vendor on the cart'),
        ('Government shops (sahakari bhandar,ration shops)','Government shops (sahakari bhandar,ration shops)'),
        ('My own nutri-garden/ Terrace garden','My own nutri-garden/ Terrace garden'),
        ('Private supermarket (DMart, Big Bazaar)','Private supermarket (DMart, Big Bazaar)'),
        ('Apmc market (apmc vashi market)','Apmc market (apmc vashi market)')
    ]

    grow_own_food_choices = [
        ('Yes, I grow my own food','Yes, I grow my own food'),
        ('No, I do not have enough space','No, I do not have enough space'),
        ('No, it\'s too expensive','No, it\'s too expensive'),
        ('No, it takes up too much time','No, it takes up too much time'),
        ('No, there\'s too much to learn','No, there\'s too much to learn'),
        ('No, I am not interested in growing food','No, I am not interested in growing food'),
    ]

    reason_gardening_choices = [
        ('Enjoy gardening','Enjoy gardening'),
        ('To grow fresh food','To grow fresh food'),
        ('Because i like flowers/ pretty garden','Because i like flowers/ pretty garden'),
        ('Because it\'s inexpensive','Because it\'s inexpensive'),
        ('N/A- if you don\'t do gardening','N/A- if you don\'t do gardening'), 
    ]

    healthy_diet_choices = [
        ('Maggie + Rice + Sprouts salad + Pepsi + Cream Biscuits + Egg','Maggie + Rice + Sprouts salad + Pepsi + Cream Biscuits + Egg'),
        ('Dal + Curd + Rice + Cucumber-carrot salad + Egg + Banana','Dal + Curd + Rice + Cucumber-carrot salad + Egg + Banana'),
        ('Paneer tikka + apple + Bread pakoda + pasta + beetroot juice + curd','Paneer tikka + apple + Bread pakoda + pasta + beetroot juice + curd'),
        ('Chicken curry + Rice + Chapati + Cheese + Cream biscuits + Dal','Chicken curry + Rice + Chapati + Cheese + Cream biscuits + Dal'),
        ('Chicken curry + rice + chapati + salad + buttermilk + orange','Chicken curry + rice + chapati + salad + buttermilk + orange')
    ]

    imp_nutrients_choices = [
        ('Vitamins','Vitamins'),
        ('Fats','Fats'),
        ('Proteins','Proteins'),
        ('Carbohydrates','Carbohydrates'),
        ('Minerals','Minerals')
    ]
    
    
    nutriGarden = forms.ChoiceField(label = ("Do you know what is a Nutri-garden?"),choices=YES_NO,widget=forms.RadioSelect(),required=False)
    source_fruits_vegetables = forms.MultipleChoiceField(label = ("Where do you buy your fruits and vegetables from?"),choices=source_fruits_vegetables_choices,widget=forms.CheckboxSelectMultiple,required=False)
    grow_own_food = forms.MultipleChoiceField(label = ("Do you grow your own food?"),choices=grow_own_food_choices,widget=forms.CheckboxSelectMultiple,required=False)
    reason_gardening = forms.ChoiceField(label = ("What is your reason for gardening?"),choices=reason_gardening_choices,widget=forms.RadioSelect(),required=False)
    healthy_diet = forms.ChoiceField(label = ("Select a Healthy Diet."),choices=healthy_diet_choices,widget=forms.RadioSelect(),required=False)
    imp_nutrients = forms.ChoiceField(label = ("Which of the following nutrients is important for body, cell, and muscle growth and repair?"),choices=imp_nutrients_choices,widget=forms.RadioSelect(),required=False)
    

    # def clean(self):
    #     print(self.cleaned_data['grow_own_food']):
    #         self.add_error('grow_own_food','REQUEIRED')
    #     return self.cleaned_data



class ModuleOneForm2(forms.ModelForm):
    class Meta:
        model = ModuleOne
        fields = ['citrus_fruits_blank', 'not_richsource_iron', 'source_vitaminA', 'imp_eat_fruits_vegetables', 'reason_wide_variety_food', 'microgreen', 'microgreen_example', 'harvestdays_microgreen']
    citrus_fruits_blank_choices=[
        ('Calcium','Calcium'),
        ('Vitamin A','Vitamin A'),
        ('Vitamin C','Vitamin C'),
        ('Iron', 'Iron')
    ]

    not_richsource_iron_choices = [
        ('Red meat','Red meat'),
        ('Spinach','Spinach'),
        ('Tea','Tea'),
        ('All of the above','All of the above'),
        ('None of the above','None of the above')
    ]
    
    source_vitaminA_choices=[('Cheese','Cheese'),
         ('Potatoes','Potatoes'),
         ('Fruits and vegetables','Fruits and vegetables'),
         ('Beans','Beans')]

    imp_eat_fruits_vegetables_choices=[('provide a lot of sugar','provide a lot of sugar'),
         ('provide vitamins and minerals','provide vitamins and minerals'),
         ('provide a lot of fat','provide a lot of fat'),
         ('provide calcium','provide calcium')]

    reason_wide_variety_food_choices=[('To learn the food label','To learn the food label'),
         ('To provide all the nutrients you need','To provide all the nutrients you need'),
         ('To keep from getting bored with your diet','To keep from getting bored with your diet'),
         ('To help improve physical fitness','To help improve physical fitness')]

    microgreen_choices=[('They are young vegetables','They are young vegetables'),
         ('They are first true leaves produced from a seedling','They are first true leaves produced from a seedling'),
         ('They are baby plants','They are baby plants'),
         ('All of the above','All of the above'),
         ('None of the above','None of the above')]


    microgreen_example_choices=[('Sprouts','Sprouts'),
         ('True Leaves','True Leaves'),
         ('Flowers','Flowers'),
         ('Roots','Roots')]

    harvestdays_microgreen_choices=[('30 days','30 days'),
         ('5-10 days','5-10 days'),
         ('60 days','60 days'),
         ('12-14 days','12-14 days')]

    
    citrus_fruits_blank = forms.ChoiceField(label = ("Citrus fruits are an excellent source of ----------?"),choices=citrus_fruits_blank_choices,widget=forms.RadioSelect(),required=False)
    not_richsource_iron = forms.ChoiceField(label = ("Which is not a rich source of iron?"),choices=not_richsource_iron_choices,widget=forms.RadioSelect(),required=False)
    source_vitaminA = forms.ChoiceField(label = ("Which of these is a common source of vitamin A?"),choices=source_vitaminA_choices,widget=forms.RadioSelect(),required=False)
    imp_eat_fruits_vegetables = forms.ChoiceField(label = ("Why is it important to eat fruits and vegetables?"),choices=imp_eat_fruits_vegetables_choices,widget=forms.RadioSelect(),required=False)
    reason_wide_variety_food = forms.ChoiceField(label = ("What is the main reason for eating a wide variety of foods?"),choices=reason_wide_variety_food_choices,widget=forms.RadioSelect(),required=False)    
    microgreen=  forms.ChoiceField(label = ("What are microgreens?"),choices=microgreen_choices, widget= forms.RadioSelect(),required=False)
    microgreen_example= forms.ChoiceField(label = ("Examples of Microgrens?"),choices=microgreen_example_choices, widget= forms.RadioSelect(),required=False)
    harvestdays_microgreen= forms.ChoiceField(label = ("How many days does it take to harvest microgreens"),choices=harvestdays_microgreen_choices, widget= forms.RadioSelect(),required=False)


class ModuleOneForm3(forms.ModelForm):
    class Meta:
        model = ModuleOne
        fields = ['microgreen_grow_seeds_kitchen', 'microgreen_nutritiousthan_fullgrownvegetables', 'microgreen_immunity', 'microgreen_variety', 'microgreen_source', 'newspaper_grow_microgreen', 'microgreen_first_step', 'soaking_time_seeds', 'microgreen_watering', 'microgreen_use']


    microgreen_variety_choices=[('Wheat','Wheat'),
         ('Radish','Radish'),
         ('Mustard','Mustard'),
         ('All of the above','All of the above'),
         ('None of the above','None of the above')]

    microgreen_source_choices=[('Plastic bottle','Plastic bottle'),
         ('tray','tray'),
         ('Thali','Thali'),
         ('All of the above','All of the above'),
         ('None of the above','None of the above')]


    True_False=[('True','True'),
         ('False','False')]
    
    microgreen_first_step_choices=[('To add soil in the container','To add soil in the container'),
         ('To wash the seeds','To wash the seeds'),
         ('Soak the seeds in water','Soak the seeds in water'),
         ('To spread seeds in the soil','To spread seeds in the soil')]
    
    soaking_time_seeds_choices=[('12 hours','12 hours'),
         ('4-5 hours','4-5 hours'),
         ('1 time a day','1 time a day'),
         ('4-5 hours','4-5 hours'),
         ('24 hours','24 hours')]

    microgreen_watering_choices=[('5 times a day','5 times a day'),
         ('2 times a day','2 times a day'),
         ('1 time a day','1 time a day'),
         ('10 times a day','10 times a day'),
         ('None of the above','None of the above')]

         
    microgreen_use_choices=[('in_sandwiches','In sandwiches'),
         ('In juice','In juice'),
         ('In paratha','In paratha'),
         ('All of the above','All of the above'),
         ('None of the above','None of the above')]

    microgreen_grow_seeds_kitchen = forms.ChoiceField(label = ("Microgreens can be grown from almost all seeds available in the kitchen."),choices=True_False, widget= forms.RadioSelect(),required=False)
    microgreen_nutritiousthan_fullgrownvegetables = forms.ChoiceField(label = ("Microgreens are more nutritious than full-grown vegetables."),choices=True_False, widget= forms.RadioSelect(),required=False)
    microgreen_immunity = forms.ChoiceField(label = ("Microgreens help in building immunity."),choices=True_False, widget= forms.RadioSelect(),required=False)
    microgreen_variety = forms.ChoiceField(label = ("What varieties can be grown in microgreens?"),choices=microgreen_variety_choices, widget= forms.RadioSelect(),required=False)
    microgreen_source = forms.ChoiceField(label = ("Where can microgreens be grown?"),choices=microgreen_source_choices, widget= forms.RadioSelect(),required=False)
    newspaper_grow_microgreen = forms.ChoiceField(label = ("Newspapers can be used as a medium to grow microgreens."),choices=True_False, widget= forms.RadioSelect(),required=False)
    microgreen_first_step = forms.ChoiceField(label = ("What is the first step to grow microgreens?"),choices=microgreen_first_step_choices, widget= forms.RadioSelect(),required=False)
    soaking_time_seeds = forms.ChoiceField(label = ("How many hours should we soak the seeds in water?"),choices=soaking_time_seeds_choices, widget= forms.RadioSelect(),required=False)
    microgreen_watering = forms.ChoiceField(label = ("How many times should microgreens be watered to keep the seed/plant moist?"),choices=microgreen_watering_choices, widget= forms.RadioSelect(),required=False)
    microgreen_use = forms.ChoiceField(label = ("How can we use a microgreen?"),choices=microgreen_use_choices, widget= forms.RadioSelect(),required=False)