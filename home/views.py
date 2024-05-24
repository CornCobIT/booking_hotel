from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Amenities, Room, RoomBooking)
from django.db.models import Q
from .forms import BookingForm

def check_booking(check_in_date, check_out_date, id, room_count):
    qs = RoomBooking.objects.filter(
        check_in_date__lte=check_in_date,
        check_out_date__gte=check_out_date,
        room__id = id
        )
    
    if len(qs) >= room_count:
        return False
    
    return True

def home(request):
    amenities_objs = Amenities.objects.all()
    rooms_objs = Room.objects.all()
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')

    if sort_by:
        if sort_by == 'ASC':
            rooms_objs = rooms_objs.order_by('room_price')
        elif sort_by == 'DSC':
            rooms_objs = rooms_objs.order_by('-room_price')

    if search:
        rooms_objs = rooms_objs.filter(Q(room_name__icontains=search) | Q(description__icontains=search))

    if amenities:
        rooms_objs = rooms_objs.filter(amenities__amenity_name__in=amenities).distinct()

    context = {
        'amenities_objs': amenities_objs,
        'rooms_objs': rooms_objs,
        'sort_by': sort_by,
        'search': search,
        'amenities': amenities,
    }
    return render(request, 'home.html', context)


def room_detail(request, id):
    room_obj = Room.objects.get(id=id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room_obj
            booking.user = request.user
            booking.save()
            messages.success(request, 'Your booking has been saved')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Failed to save booking. Please check your input.')
    else:
        form = BookingForm()
        
    context = {
        'room_obj': room_obj,
        'form': form
    }

    return render(request, 'room_detail.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        request.session['user_id'] = user_obj.id
        return redirect('/')

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'register.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def about_us(request):
    return render(request, 'about_us.html')

def booking(request):
    rooms_objs = Room.objects.all()
    context = {
        'rooms_objs': rooms_objs,
    }
    return render(request, 'booking.html', context)

def all_room(request):
    rooms_objs = Room.objects.all()
    context = {
        'rooms_objs': rooms_objs,
    }
    return render(request, 'all_room.html', context)
