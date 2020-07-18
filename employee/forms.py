from django import forms
from .models import Employee,EmployeeAccount,BorrowTransaction
from django.contrib.auth.forms import UserCreationForm
from items.models import Item

class Employee_Form(forms.ModelForm):
    
    class Meta:
        model = Employee
        fields = ('fullname', 'employee_nik', 'position', 'division', 'sex', 'address')
        labels = {
            'fullname':'Fullname',
            'employee_nik':'NIK',
            'division':'Division',
            'address':'Address',
            'sex':'Sex',
        }

    def __init__(self,*args,**kwargs):
        super(Employee_Form,self).__init__(*args,**kwargs)
        self.fields['position'].empty_label = "Select"
        self.fields['sex'].empty_label = None
        self.fields['division'].empty_label = None

class CreateUserEmployee(UserCreationForm):
    username = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    class Meta:
        model = EmployeeAccount
        fields = ("username","email","password1","password2")
    def save(self,commit=True):
        user = super(CreateUserEmployee,self).save(commit=False)
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

class DateInput(forms.DateInput):
    input_type = 'date'

class BorrowForm(forms.ModelForm):
    borrow_date = forms.DateField()

    class Meta:
        model = BorrowTransaction
        fields = ('employee_nik','borrow_date','item_name', 'project_location', 'return_date')
        labels = {
            'employee_nik':'Employee Name',
            'item_name':'Item Name',
            'project_location':'Project Location',
        }
        widgets = {
            'borrow_date':forms.DateInput(attrs={'class':'MyDate'}),
        }
    def __init__(self,*args,**kwargs):
        super(BorrowForm,self).__init__(*args,**kwargs)
        self.fields['item_name'].queryset = Item.objects.filter(active = True)
        self.fields['return_date'].disabled=True

class ReturnForm(forms.ModelForm):
    return_date = forms.DateField(required=True)

    class Meta:
        model = BorrowTransaction
        fields = ('employee_nik','borrow_date','item_name', 'project_location', 'return_date')
        labels = {
            'employee_nik':'Employee Name',
            'item_name':'Item Name',
            'project_location':'Project Location',
            'borrow_date':'Borrow Date',
        }
        widgets = {
            'return_date':forms.DateInput(attrs={'class':'MyDateReturn'}),
        }
    def __init__(self,*args,**kwargs):
        super(ReturnForm,self).__init__(*args,**kwargs)
        self.fields['item_name'].disabled = True
        self.fields['employee_nik'].disabled = True
        self.fields['project_location'].disabled = True
        self.fields['borrow_date'].disabled = True