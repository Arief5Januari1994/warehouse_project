from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.item_form,name='item_insert'),
    path('<int:id>/', views.item_form,name='item_update'),
    path('delete/<int:id>/', views.item_delete,name='item_delete'),
    path('list/', views.item_list,name='item_list'),
    path('history/', views.history_service_form,name='history_insert'),
    path('history/update/<str:item_history_service_id>/', views.history_service_form,name='history_update'),
    path('history/delete/<str:item_history_service_id>/', views.history_service_delete,name='history_delete'),
    path('history/list/', views.history_service_list,name='history_list'),
    path('history/detail/<str:item_history_service_id>', views.history_service_detail,name='history_detail'),
    path('borrow/export/pdf/', views.pdf_report_item_history, name='export_report_item_history'),
    path('history/export/pdf/<str:item_history_service_id>/', views.pdf_item_history, name='export_item_history'),
]