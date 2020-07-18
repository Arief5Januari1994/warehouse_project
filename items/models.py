from django.db import models
from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_name = models.CharField(max_length = 200)
    item_code = models.CharField(max_length = 8)
    item_merk = models.CharField(max_length = 100)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    item_picture = models.ImageField(blank=True,upload_to='album_item/',default='album_item/no-image.jpg')
    active = models.BooleanField('Active or not', blank=True, default=True)

    def __str__(self):
        return self.item_name

class ItemHistoryService(models.Model):
    # AutoIncrementID
    def increment_service_number():
        last_service = ItemHistoryService.objects.all().order_by('item_history_service_id').last()

        if not last_service:
            return 'SERV-'+ str(datetime.now().strftime('%d%m%Y-'))+'0000'

        service_id = last_service.item_history_service_id
        service_int = service_id[14:18]
        new_service_int = int(service_int)+1
        new_service_id = 'SERV-'+ str(datetime.now().strftime('%d%m%Y-'))+str(new_service_int).zfill(4)

        return new_service_id

    item_history_service_id = models.CharField(max_length=20,primary_key=True,unique=True,default=increment_service_number)
    item_name = models.ForeignKey('items.Item',on_delete=models.CASCADE,related_name='items_set')
    service_by = models.ForeignKey('employee.Employee',on_delete=models.CASCADE,related_name='employee_set')
    service_date = models.DateField()
    detail_service = models.TextField(max_length = 800)
    picture = models.ImageField(blank=True,upload_to='album_history/',default='album_history/no-image.jpg')

    def __str__(self):
        return self.item_history_service_id