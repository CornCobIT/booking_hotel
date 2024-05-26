from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import *
from django.db.models import Q
from .forms import BookingForm
from .utils import calculate_nights, calculate_total_price, calculate_points
from django.utils import timezone


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

    if 'booking_success' in request.session:
        messages.success(request, request.session.pop('booking_success'))
    context = {
        'amenities_objs': amenities_objs,
        'rooms_objs': rooms_objs,
        'sort_by': sort_by,
        'search': search,
        'amenities': amenities,
    }
    return render(request, 'home.html', context)

def calculate_total_price_for_form(form, room_price):
    check_in_date = form.cleaned_data.get('check_in_date')
    check_out_date = form.cleaned_data.get('check_out_date')
    num_rooms = form.cleaned_data.get('num_rooms')

    if not check_in_date or not check_out_date or not num_rooms:
        return 0

    total_price = calculate_total_price(room_price, num_rooms, check_in_date, check_out_date)

    return total_price

def room_detail(request, id):
    room_obj = get_object_or_404(Room, id=id)
    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        submit_type = request.POST.get('submit_type')
        booking.room = room_obj
        today = timezone.now().date()

        if booking.guests > room_obj.capacity * booking.num_rooms:
            messages.warning(request, 'The number of guests error.')
        elif booking.check_out_date <= booking.check_in_date:
            messages.warning(request, 'Check-out date must be after check-in date.')
        elif booking.check_in_date < today:
            messages.warning(request, 'Check-in date cannot be in the past.')
        elif booking.guests <= 0:
            messages.warning(request, 'Number of guests must be greater than 0.')
        elif booking.num_rooms <= 0:
            messages.warning(request, 'Number of rooms must be greater than 0.')
        else:
            booking.user = request.user
            if submit_type == 'next':
                booking.save()
            else:
                return redirect('home')
            return redirect('payment', booking_id=booking.id)

    elif form.errors:
        messages.error(request, 'Failed to save booking. Please check your input.')

    context = {
        'room_obj': room_obj,
        'form': form,
    }
    return render(request, 'room_detail.html', context)

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id)
    total_price = booking.total_price 
    room_obj = booking.room

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        submit_type = request.POST.get('submit_type')
        booking.payment_method = payment_method
        if submit_type == 'next' or submit_type == 'done':
            booking.save()
        if payment_method in ['paypal', 'credit_card', 'debit_card']:
            return redirect('qr_payment', booking_id=booking.id)
        return redirect('home')

    context = {
        'booking': booking,
        'total_price': total_price,
        'room_obj': room_obj,
    }
    return render(request, 'payment.html', context)

@login_required
def qr_payment(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id)
    total_price = booking.total_price

    context = {
        'booking': booking,
        'total_price': total_price,
    }
    return render(request, 'qr_payment.html', context)


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

    return render(request ,'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Account with this username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Account with this email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username=username)
        user.set_password(password)
        user.email = email
        user.save()

        UserProfile.objects.create(user=user)

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login_page')

    return render(request, 'register.html')

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

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'profile': user_profile,
    }
    return render(request, 'profile.html', context)

