from django import forms
from .models import Item,ItemHistoryService

class ItemForms(forms.ModelForm):
    item_picture = forms.FileField()

    class Meta:
        model = Item
        fields = ('item_name', 'item_code', 'item_merk', 'category', 'item_picture')
        labels = {
            'item_name':'Item Name',
            'item_code':'Item Code',
            'item_merk':'Item Merk',
            'item_picture':'Item Picture',
        }
    
    def __init__(self,*args,**kwargs):
        super(ItemForms,self).__init__(*args,**kwargs)
        self.fields['category'].empty_label = "Select"
        self.fields['item_code'].required = True

class DateInput(forms.DateInput):
    input_type = 'date'

class ItemHistoryServiceForm(forms.ModelForm):
    service_date = forms.DateField()
    picture = forms.FileField()
    class Meta:
        model = ItemHistoryService
        fields = ('item_history_service_id','item_name','service_by','service_date','detail_service','picture')
        labels = {
            'item_history_service_id':'Item History Service ID',
            'item_name':'Item Name',
            'service_by':'Service By',
            'service_date':'Service Date',
            'detail_service':'Detail Service',
            'picture':'Insert Picture',
        }
        widgets = {
            'service_date':forms.DateInput(attrs={'class':'MyDate'}),
        }

    def __init__(self,*args,**kwargs):
        super(ItemHistoryServiceForm,self).__init__(*args,**kwargs)
        self.fields['item_name'].empty_label="Select"