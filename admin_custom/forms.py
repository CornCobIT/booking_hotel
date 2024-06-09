from django import forms
from django.contrib.auth import get_user_model
from home.models import *

User = get_user_model()

class UserForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False, label='Is Admin')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_admin']
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
            'first_name': 'Họ',
            'last_name': 'Tên',
            'is_admin': 'Quyền Admin',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_admin']
        user.is_superuser = self.cleaned_data['is_admin']
        self.fields['is_admin'].label = "Quyền hạn"
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'address', 'phone', 'avatar', 'points']
        labels = {
            'bio': 'Ghi chú',
            'birth_date': 'Ngày sinh',
            'address': 'Địa chỉ',
            'phone': 'Số điện thoại',
            'points': 'Điểm tích lũy'
        }
        
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'description', 'address', 'phone_number', 'image']
        labels = {
            'hotel_name': 'Tên khách sạn',
            'description': 'Mô tả',
            'address': 'Địa chỉ',
            'phone_number': 'Số điện thoại',
            'image': 'Ảnh',
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'room_name', 'description', 'price', 'amenities', 'capacity', 'room_status', 'room_count']
        labels = {
            'hotel': 'Khách sạn',
            'room_name': 'Tên phòng',
            'description': 'Mô tả',
            'price': 'Giá tiền',
            'amenities': 'Tiện ích',
            'capacity': 'Sức chứa',
            'room_status': 'Trạng thái phòng',
            'room_count': 'Số lượng phòng'
        }

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['room', 'user', 'check_in_date', 'check_out_date', 'guests', 'num_rooms', 'payment_method', 'payment_status', 'booking_status', 'total_price']
        labels = {
            'room': 'Phòng',
            'user': 'Người dùng',
            'check_in_date': 'Ngày nhận phòng',
            'check_out_date': 'Ngày trả phòng',
            'guests': 'Số lượng khách',
            'num_rooms': 'Số lượng phòng đặt',
            'payment_method': 'Phương thức thnh toán',
            'payment_status': 'Trạng thái thanh toán',
            'booking_status': 'Trạng thái đặt phòng',
            'total_price': 'Tổng tiền',
        }
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['room', 'user', 'rating', 'comment']
        labels = {
            'room': 'Phòng',
            'user': 'Người dùng',
            'rating': 'Điểm đánh giá',
            'comment': 'Nhận xét'
        }
        
class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImages
        fields = ['room', 'images']
        labels = {
            'room': 'Phòng',
            'images': 'Ảnh'
        }