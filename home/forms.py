from django import forms
from .models import RoomBooking, UserProfile, User
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):

    class Meta:
        model = RoomBooking
        fields = ['check_in_date', 'check_out_date', 'guests', 'num_rooms']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in_date'].initial = datetime.now().date()
        self.fields['check_out_date'].initial = (datetime.now() + timedelta(days=2)).date()
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone', 'avatar']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']