from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.employee_form,name='employee_insert'),
    path('<int:employee_nik>/', views.employee_form,name='employee_update'),
    path('delete/<int:id>/', views.employee_delete,name='employee_delete'),
    path('list/', views.employee_list,name='employee_list'),
    path('login/', views.login_view,name='login_view'),
    path('register/', views.register,name='register'),
    path('borrow/', views.borrow_form,name='borrow_insert'),
    path('borrow/<int:id>/', views.borrow_form,name='borrow_update'),
    path('borrow/delete/<int:id>/', views.borrow_delete,name='borrow_delete'),
    path('borrow/list/', views.borrow_list,name='borrow_list'),
    path('borrow/export/pdf/', views.pdf_view, name='export_data'),
    path('borrow/export/pdf/<int:id>/', views.pdf_borrow_view, name='export_data_borrow'),
]