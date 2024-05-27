from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import *
from django.db.models import Q
from .forms import BookingForm, ProfileForm, UserForm, ReviewForm
from .utils import calculate_nights, calculate_total_price, calculate_points
from django.utils import timezone
from django.urls import reverse
import re


def handler404(request, exception):
    return render(request, '404.html', status=404)


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
    reviews = Review.objects.filter(room=room_obj)

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
            user_profile = UserProfile.objects.get(user=request.user)
            booking.user = user_profile
            if submit_type == 'next':
                booking.save()
                return redirect('payment', booking_id=booking.id)
            else:
                return redirect('home')

    elif form.errors:
        messages.error(request, 'Failed to save booking. Please check your input.')

    context = {
        'room_obj': room_obj,
        'form': form,
        'reviews': reviews
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

        user_obj = User.objects.filter(username=username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request, user_obj)
        request.session['user_id'] = user_obj.id
        return redirect('/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Kiểm tra username và email đã tồn tại hay chưa
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Account with this username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Account with this email already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Kiểm tra mật khẩu phức tạp
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_pattern, password):
            messages.warning(request,
                             'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Kiểm tra mật khẩu và xác nhận mật khẩu khớp nhau
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Tạo user mới và băm mật khẩu
        user = User.objects.create_user(username=username, email=email, password=password)
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
    bookings = user_profile.bookings.filter(booking_status='confirmed', payment_status='completed')

    total_points = 0
    for booking in bookings:
        points = calculate_points(booking.total_price)
        total_points += points

    user_profile.points += total_points
    user_profile.save()

    context = {
        'profile': user_profile,
        'user_email': request.user.email,
        'total_points': total_points
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id).user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserForm(request.POST, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            user_instance = user_form.save(commit=False)
            profile_instance.save()
            user_instance.save()

            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserForm(instance=user)

    return render(request, 'edit_profile.html', {'profile_form': profile_form, 'user_form': user_form})


@login_required
def booking_management(request, user_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    bookings = RoomBooking.objects.filter(user=profile)
    context = {
        'profile': profile,
        'bookings': bookings,
    }
    return render(request, 'booking_management.html', context)


def booking_detail(request, user_id, booking_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    booking = get_object_or_404(RoomBooking, id=booking_id, user=profile)
    total_price = calculate_total_price(
        booking.room.price,
        booking.num_rooms,
        booking.check_in_date,
        booking.check_out_date
    )
    nights = calculate_nights(booking.check_in_date, booking.check_out_date)
    points = calculate_points(total_price)
    context = {
        'profile': profile,
        'booking': booking,
        'total_price': total_price,
        'nights': nights,
        'points': points,
    }
    return render(request, 'booking_detail.html', context)


@login_required
def cancel_booking(request, user_id, booking_id):
    profile = get_object_or_404(UserProfile, id=user_id)
    booking = get_object_or_404(RoomBooking, id=booking_id, user=profile)

    if request.method == "POST":
        if booking.booking_status == 'pending':
            booking.booking_status = 'cancelled'
            booking.save()
            messages.success(request, 'Your booking has been successfully cancelled.')
        else:
            messages.error(request, 'Booking cancellation failed.')
        return redirect('booking_management', user_id=user_id)

    messages.error(request, 'Invalid request method.')
    return redirect('booking_management', user_id=user_id)


@login_required
def create_review(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id, user=request.user.profile)

    # Kiểm tra trạng thái booking và payment
    if booking.booking_status != 'confirmed' or booking.payment_status != 'completed':
        messages.warning(request, 'You can only leave a review after your booking is confirmed and paid.')
        return redirect('booking_detail', user_id=booking.user.id, booking_id=booking.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = booking.room
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('booking_detail', user_id=booking.user.id, booking_id=booking.id)
    else:
        form = ReviewForm()

    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'create_review.html', context)

