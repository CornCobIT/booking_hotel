from django.urls import path
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
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()