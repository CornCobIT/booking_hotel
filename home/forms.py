from django import forms
from .models import RoomBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in_date', 'check_out_date', 'guests', 'payment_method']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}),
            'payment_method': forms.Select(choices=RoomBooking.payment_method, attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date and check_in_date >= check_out_date:
            raise forms.ValidationError("Check-out date must be after check-in date.", code='invalid_date_range')

        return cleaned_data
