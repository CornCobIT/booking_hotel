from django.contrib import admin

# Register your models here.
from .models import *

class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('amenities',)
    list_display = ('room_name', 'hotel', 'price', 'room_status', 'room_count',)

class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'check_in_date', 'check_out_date', 'payment_method', 'payment_status', 'booking_status']
    list_filter = ['payment_status', 'booking_status']
    search_fields = ['room__room_name', 'user__username']
    readonly_fields = []

admin.site.register(Amenities)
admin.site.register(Room, RoomAdmin)
admin.site.register(Hotel)
admin.site.register(RoomImages)
admin.site.register(RoomBooking, RoomBookingAdmin)