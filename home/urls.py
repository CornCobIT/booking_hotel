from django.urls import path
from django.conf.urls import handler404
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home , name='home'),
    path('room/<uuid:id>/', room_detail, name="room_detail"),
    path('payment/<uuid:booking_id>/', payment, name='payment'),
    path('qr_payment/<uuid:booking_id>/', qr_payment, name='qr_payment'),
    path('login/', login_page , name='login_page'),
    path('register/', register_page , name='register_page'),
    path('logout/', logout , name='logout'),
    path('about_us/', about_us, name='about_us'),
    path('booking/', booking, name='booking'),
    path('all_room/', all_room, name='all_room'),
    path('profile/', profile, name='profile'), 
    path('booking_management/<uuid:user_id>/', booking_management, name='booking_management'),
    path('booking_detail/<uuid:user_id>/<uuid:booking_id>/', booking_detail, name='booking_detail'),
    path('cancel_booking/<uuid:user_id>/<uuid:booking_id>/', cancel_booking, name='cancel_booking'),
    path('edit_profile/<uuid:user_id>/', edit_profile, name='edit_profile'),
]

handler404 = handler404

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()