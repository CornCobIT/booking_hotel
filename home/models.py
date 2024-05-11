from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings

import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateField(default=timezone.now)
    updated_at = models.DateField(default=timezone.now)

    class Meta:
        abstract = True


class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200, default='')
    phone_number = models.CharField(max_length=20, default='')
    image = models.ImageField(null=True, blank=True, upload_to='hotel_img')
    def __str__(self):
        return self.hotel_name

class Room(BaseModel):
    hotel= models.ForeignKey(Hotel, on_delete=models.CASCADE, default='')  
    room_number = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    amenities = models.ManyToManyField(Amenities)
    ROOM_VALUE = (
        ('1', 'Still'),
        ('0', 'Out of room'),
    )
    room_status = models.CharField(choices=ROOM_VALUE, default='1', max_length=10)
    room_count = models.IntegerField(default=1)
    def get_first_image(self):
        try:
            return self.images.first().image.url
        except AttributeError:
            return None
        
    def __str__(self):
        return f"Room {self.room_number}"

class RoomImages(BaseModel):
    room= models.ForeignKey(Room ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="room_img")
    
    def __str__(self) -> str:
        return self.room.room_name



class RoomBooking(BaseModel):
    room = models.ForeignKey(Room, related_name="room_bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_bookings", on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=(
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ))
    payment_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ), default='pending')
    booking_status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ), default='pending')

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.room_name} from {self.check_in_date} to {self.check_out_date}"

class Review(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()

class UserProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

class FacebookProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)