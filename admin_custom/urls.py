from django.urls import path, include
from django.conf.urls import handler404
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('amenities/', amenities, name='admin_amenities'),
    path('amenities/add/', add_amenity, name='add_amenity'),
    path('amenities/edit/<uuid:amenity_id>/', edit_amenity, name='edit_amenity'),
    path('amenities/delete/<uuid:amenity_id>/', delete_amenity, name='delete_amenity'),
    # Users
    path('user_profiles/', user_profile_list, name='user_profile_list'),
    path('user_profiles/add/', add_user_profile, name='add_user_profile'),
    path('user_profiles/edit/<int:user_id>/', edit_user_profile, name='edit_user_profile'),
    path('user_profiles/delete/<int:user_id>/', delete_user_profile, name='delete_user_profile'),

    # Hotels
    path('hotels/', hotel_list, name='admin_hotels'),
    path('hotels/add/', add_hotel, name='add_hotel'),
    path('hotels/edit/<uuid:hotel_id>/', edit_hotel, name='edit_hotel'),
    path('hotels/delete/<uuid:hotel_id>/', delete_hotel, name='delete_hotel'),

    # Rooms
    path('rooms/', room_list, name='admin_rooms'),
    path('rooms/add/', add_room, name='add_room'),
    path('rooms/edit/<uuid:room_id>/', edit_room, name='edit_room'),
    path('rooms/delete/<uuid:room_id>/', delete_room, name='delete_room'),

    # Room Images
    path('room_images/', room_images_list, name='admin_room_images'),
    path('room_images/add/', add_room_image, name='add_room_image'),
    path('room_images/edit/<uuid:image_id>/', edit_room_image, name='edit_room_image'),
    path('room_images/delete/<uuid:image_id>/', delete_room_image, name='delete_room_image'),

    # Bookings
    path('bookings/', booking_list, name='admin_bookings'),
    path('bookings/add/', add_booking, name='add_booking'),
    path('bookings/edit/<uuid:booking_id>/', edit_booking, name='edit_booking'),
    path('bookings/delete/<uuid:booking_id>/', delete_booking, name='delete_booking'),

    # Reviews
    path('reviews/', review_list, name='admin_reviews'),
    path('reviews/add/', add_review, name='add_review'),
    path('reviews/edit/<uuid:review_id>/', edit_review, name='edit_review'),
    path('reviews/delete/<uuid:review_id>/', delete_review, name='delete_review'),
]

handler404 = handler404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
