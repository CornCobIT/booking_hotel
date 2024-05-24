from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('check_booking/' , check_booking),
    path('', home , name='home'),
    path('room-detail/<id>/', room_detail, name="room_detail"),
    path('login/', login_page , name='login_page'),
    path('register/', register_page , name='register_page'),
    path('logout/', logout , name='logout'),
    path('about_us/', about_us, name='about_us'),
    path('booking/', booking, name='booking'),
    path('all_room/', all_room, name='all_room'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()