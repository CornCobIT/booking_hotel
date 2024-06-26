from django import forms
from .models import RoomBooking, UserProfile, User, Review
from datetime import datetime, timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['check_in_date', 'check_out_date', 'guests', 'num_rooms']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'check_in_date': 'Ngày nhận phòng',
            'check_out_date': 'Ngày trả phòng',
            'guests': 'Số khách',
            'num_rooms': 'Số phòng'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in_date'].initial = datetime.now().date()
        self.fields['check_out_date'].initial = (datetime.now() + timedelta(days=2)).date()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone', 'avatar']
        labels = {
            'address': 'Địa chỉ',
            'phone': 'Số điện thoại',
            'avatar': 'Ảnh đại diện'
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email'
        }


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Đánh giá',
            'comment': 'Bình luận'
        }
