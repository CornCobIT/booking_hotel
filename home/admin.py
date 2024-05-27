from django.contrib import admin
from .utils import calculate_nights, calculate_total_price, calculate_points

# Register your models here.
from .models import *

class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('amenities',)
    list_display = ('room_name', 'hotel', 'price', 'room_status', 'room_count',)

class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'check_in_date', 'check_out_date', 'payment_method', 'payment_status', 'booking_status', 'total_price']
    list_filter = ['payment_status', 'booking_status']
    search_fields = ['room__room_name', 'user__username']
    readonly_fields = []

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'fullname', 'email', 'phone', 'points']

    def username(self, obj):
        return obj.user.username if obj.user else None
    username.short_description = 'Username'

    def fullname(self, obj):
        return obj.fullname
    fullname.short_description = 'Full Name'

    def email(self, obj):
        return obj.user.email if obj.user else None
    
admin.site.register(Amenities)
admin.site.register(Room, RoomAdmin)
admin.site.register(Hotel)
admin.site.register(RoomImages)
admin.site.register(RoomBooking, RoomBookingAdmin)
admin.site.register(UserProfile, ProfileAdmin)