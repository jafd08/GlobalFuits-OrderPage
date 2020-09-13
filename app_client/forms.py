from django import forms

from app_order.models import Order


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



class OrderCreateForm(BaseForm, forms.ModelForm):
    date = forms.DateField(label="Fecha de Entrega", widget=forms.DateInput(attrs={'type': 'date', 'style':'width:auto'}))
    #requestor = forms.ChoiceField(widget=forms.Select(attrs={'disabled': 'disabled'}))
    title = forms.CharField(label="Titulo", widget=forms.TextInput(attrs={'style':'width:auto'}))
    class Meta:
        model = Order
        #fields = ['requestor','date', 'title' , ]
        fields = ['title','date' ]


class OrderEditForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Order
        #fields = ['date', 'title', 'discount', 'is_paid']
        fields = []