from django.db import models
from items.models import Item
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User,AbstractBaseUser

# Create your models here.

class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    sex_choices = {
        ('','Select'),
        ('Female', 'Female'),
        ('Male', 'Male'),
    }

    division_choices = {
        ('','Select'),
        ('Manajemen Direksi','Manajemen Direksi'),
        ('HSE', 'HSE'),
        ('Lapangan', 'Lapangan'),
        ('Keuangan', 'Keuangan'),
    }
        
    fullname = models.CharField(max_length=200)
    employee_nik = models.BigIntegerField(primary_key=True)
    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    division = models.CharField(max_length=200,choices=division_choices)
    sex = models.CharField(max_length=50,choices=sex_choices, blank=False, default='')
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.fullname

class EmployeeAccount(models.Model):
    account = models.OneToOneField(User,on_delete=models.CASCADE)
    worker = models.ForeignKey(Employee,on_delete=models.CASCADE)
    username = models.CharField('username',unique = True,max_length=255)
    email = models.EmailField('email address',unique = True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.worker.fullname

class BorrowTransaction(models.Model):
    employee_nik = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employes')
    borrow_date = models.DateField()
    item_name = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='items')
    project_location = models.CharField(max_length=300)
    return_date = models.DateField(null = True, blank = True)

    def __str__(self):
        return self.id