from django.shortcuts import render,redirect
from .models import Employee,EmployeeAccount,BorrowTransaction
from .forms import Employee_Form,CreateUserEmployee,BorrowForm,ReturnForm
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from items.models import Item
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import csv
from django.http import HttpResponse,HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import sys

# Create your views here.

def employee_list(request):
    # context = {'employee_list':Employee.objects.all()}
    employee_list = Employee.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(employee_list,10)
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)
    return render(request,"employee/employee_list.html",{'employee_list':employees})

def employee_form(request,employee_nik=0,id=0):
    if request.method=='GET':
        if employee_nik==0:
            form=Employee_Form()

        else:
            employee = Employee.objects.get(pk = employee_nik)
            form = Employee_Form(instance=employee)
        return render(request,"employee/employee_form.html",{'form':form})

    else:
        if employee_nik==0:
            form=Employee_Form(request.POST)
        else:
            employee = Employee.objects.get(pk = employee_nik)
            form = Employee_Form(request.POST, instance=employee)
        if form.is_valid():
            form.save()
        return redirect('/employee/list')

def employee_delete(request,id):
    employee = Employee.objects.get(pk = id)
    employee.delete() 
    return redirect('/employee/list')

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect('employee/list')
            else:
                messages.error(request,'Username or Password Incorrect')
        else:
            messages.error(request,"Invalid Username or Password")
    form = AuthenticationForm()
    return render(request = request,template_name = 'employee/login.html',context = {"form":form})

def logout_view(request):
    logout(request)
    return redirect('/login')

def register(request):
    if request.method=='POST':
        form = CreateUserEmployee(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request,user)
            return redirect("employee/list")
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            return render(request=request,template_name = "employee/register.html",context = {"form":form})
    form = CreateUserEmployee
    return render(request=request,template_name = "employee/register.html",context = {"form":form})

def borrow_list(request):
    
    # context = {
    # 'borrow_list': BorrowTransaction.objects.all(), 
    # }
    borrow_list = BorrowTransaction.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(borrow_list,10)
    try:
        borrows = paginator.page(page)
    except PageNotAnInteger:
        borrows = paginator.page(1)
    except EmptyPage:
        borrows = paginator.page(paginator.num_pages)
    
    return render(request,"borrow/borrow_list.html",{'borrow_list':borrows})

def borrow_form(request,id = 0):
    if request.method=='GET':
        if id==0:
            form=BorrowForm()
            return render(request,"borrow/borrow_form.html",{'form':form})
        else:
            borrow = BorrowTransaction.objects.get(pk = id)
            form = ReturnForm(instance=borrow)
            borrow.item_name.active = True
            borrow.item_name.save()
            item = Item.objects.get(pk = form['item_name'].value())
            item.active = True
            item.save()
            return render(request,"borrow/return_form.html",{'form':form})
        
    else:
        if id==0:
            form=BorrowForm(request.POST)
            insert = True
        else:
            borrow = BorrowTransaction.objects.get(pk = id)
            form = ReturnForm(request.POST, instance=borrow)
            insert=False
        if insert == True and form.is_valid():
            form.save()
            item = Item.objects.get(pk = form['item_name'].value())
            item.active = False
            item.save()
        if form.is_valid():
            form.save()
        return redirect('/employee/borrow/list')

def borrow_delete(request,id):
    borrow = BorrowTransaction.objects.get(pk = id)
    borrow.delete() 
    return redirect('/employee/borrow/list')

# def file_load_view(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attatchment; filename="report_borrow.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['Employee NIK', 'Employee Name', 'Item Name', 'Item Code', 'Project Location', 'Borrow Date', 'Return Date'])
#     borrows = BorrowTransaction.objects.select_related('employee_nik', 'item_name')
#     borrows = borrows.values_list('employee_nik_id', 'employee_nik__fullname', 'item_name__item_name', 'item_name__item_code', 'project_location', 'borrow_date', 'return_date')
#     for borrow in borrows:
#         writer.writerow(borrow)
#     return response

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf8')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def pdf_view(request):
    borrows = BorrowTransaction.objects.select_related('employee_nik', 'item_name')
    params = {
        'borrows': borrows,
        'request': request,
    }
    return render_to_pdf('borrow/pdf.html',params)

def pdf_borrow_view(request,id):
    borrows = BorrowTransaction.objects.get(pk=id)
    params = {
        'borrow': borrows,
        'request': request,
    }
    return render_to_pdf('borrow/pdf_borrow.html',params)