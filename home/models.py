from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from .utils import calculate_total_price, calculate_points

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


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    points = models.IntegerField(default=0)

    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.user.username


class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200, default='')
    phone_number = models.CharField(max_length=20, default='')
    image = models.ImageField(null=True, blank=True, upload_to='hotel_img')

    def __str__(self):
        return self.hotel_name


class Room(BaseModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default='')
    room_name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    amenities = models.ManyToManyField(Amenities)
    capacity = models.IntegerField(default=2)
    ROOM_VALUE = (
        ('1', 'Still'),
        ('0', 'Out of room'),
    )
    room_status = models.CharField(choices=ROOM_VALUE, default='1', max_length=10)
    room_count = models.IntegerField(default=1)

    def __str__(self):
        return f"Room {self.room_name}"


class RoomImages(BaseModel):
    room = models.ForeignKey(Room, related_name="images", on_delete=models.SET_NULL, null=True, blank=True)
    images = models.ImageField(upload_to='room_img')

    def __str__(self):
        return f"Image for {self.room.room_name}"


class RoomBooking(BaseModel):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    room = models.ForeignKey(Room, related_name="room_bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name="bookings", on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField(default=1)
    num_rooms = models.IntegerField(default=1)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.CharField(max_length=255, choices=PAYMENT_STATUS_CHOICES, default='pending')
    booking_status = models.CharField(max_length=255, choices=BOOKING_STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Booking by {self.user.user.username} for {self.room.room_name} from {self.check_in_date} to {self.check_out_date}"

    def save(self, *args, **kwargs):
        self.total_price = calculate_total_price(self.room.price, self.num_rooms, self.check_in_date,
                                                 self.check_out_date)
        super().save(*args, **kwargs)


class Review(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.room.room_name}"
