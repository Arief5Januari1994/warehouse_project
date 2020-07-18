from django.shortcuts import render,redirect
from .forms import ItemForms, ItemHistoryServiceForm
from .models import Item, ItemHistoryService
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse,HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import sys

# Create your views here.

def item_list(request):
    # context = {'item_list':Item.objects.all()}
    item_list = Item.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(item_list,10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request,"item/item_list.html",{'item_list':items})

def item_form(request,id = 0):
    if request.method=="GET":
        if id==0:
            form=ItemForms()

        else:
            item = Item.objects.get(pk = id)
            form = ItemForms(instance=item)
        return render(request,"item/item_form.html",{'form':form})

    else:
        if id==0:
            form=ItemForms(request.POST,request.FILES)
        else:
            item = Item.objects.get(pk = id)
            form = ItemForms(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_picture=form.cleaned_data['item_picture']
            form.save()
        return redirect('/item/list')

def item_delete(request,id):
    item = Item.objects.get(pk = id)
    item.delete() 
    return redirect('/item/list')

def history_service_list(request):
    # context = {
    # 'history_service_list': ItemHistoryService.objects.all(),
    # }

    history_service_list = ItemHistoryService.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(history_service_list,10)
    try:
        history_service = paginator.page(page)
    except PageNotAnInteger:
        history_service = paginator.page(1)
    except EmptyPage:
        history_service = paginator.page(paginator.num_pages)
    
    return render(request,"history_service/item_history_service_list.html",{'history_service_list':history_service})

def history_service_form(request,item_history_service_id = 0):
    
    if request.method=='GET':
        if item_history_service_id==0:
            form=ItemHistoryServiceForm()

        else:
            try :
                history_service = ItemHistoryService.objects.get(pk = item_history_service_id)
            except ItemHistoryService.DoesNotExist:
                history_service = None             
            form = ItemHistoryServiceForm(instance=history_service)
        return render(request,"history_service/item_history_service_form.html",{'form':form})

    else:
        if item_history_service_id==0:
            form=ItemHistoryServiceForm(request.POST,request.FILES)
        else:
            history_service = ItemHistoryService.objects.get(pk = item_history_service_id)
            form = ItemHistoryServiceForm(request.POST, request.FILES, instance=history_service)
        if form.is_valid():
            picture=form.cleaned_data['picture']
            form.save()
        return redirect('/item/history/list')

def history_service_delete(request,item_history_service_id):
    history_service = ItemHistoryService.objects.get(pk = item_history_service_id)
    history_service.delete() 
    return redirect('/item/history/list')

def history_service_detail(request,item_history_service_id):
    context = {
        'history' : ItemHistoryService.objects.get(pk = item_history_service_id)
    }
    return render(request,'history_service/item_history_service_detail.html',context)

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf8')),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def pdf_report_item_history(request):
    histories = ItemHistoryService.objects.select_related('item_name', 'service_by')
    params = {
        'histories': histories,
        'request': request,
    }
    return render_to_pdf('history_service/pdf_report_item_history_service.html',params)

def pdf_item_history(request,item_history_service_id):
    histories = ItemHistoryService.objects.get(pk=item_history_service_id)
    params = {
        'history': histories,
        'request': request,
    }
    return render_to_pdf('history_service/pdf_item_history_service.html',params)