from django.contrib import admin

# Register your models here.
from .models import *

class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('amenities',)
    
admin.site.register(Amenities)
admin.site.register(Room, RoomAdmin)
admin.site.register(Hotel)
admin.site.register(RoomImages)
admin.site.register(RoomBooking)