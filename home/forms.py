from django import forms
from .models import RoomBooking
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in_date', 'check_out_date', 'guests', 'num_rooms', 'payment_method']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(choices=RoomBooking.payment_method.field.choices, attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].initial = 'cash'
        self.fields['check_in_date'].initial = datetime.now().date()
        self.fields['check_out_date'].initial = (datetime.now() + timedelta(days=2)).date()