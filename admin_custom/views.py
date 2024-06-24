from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from home.models import *
from .forms import *

# Create your views here.

def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/dashboard')
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.info(request, 'Không tìm thấy tài khoản!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            user_obj = authenticate(username=username, password=password)
            
            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/dashboard')
            
            messages.info(request, 'Mật khẩu không hợp lệ!')
            return redirect('/')
        return render(request, 'admin_login.html')
    
    except Exception as e:
        print(e)

def admin_dashboard(request):
    return render(request, 'dashboard.html')

def admin_logout(request):
    logout(request)
    return redirect('home')

# User views
User = get_user_model()

@login_required
def user_profile_list(request):
    users = User.objects.all()
    return render(request, 'user_profile_list.html', {'users': users})

@login_required
def update_user_role(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        role = request.POST.get('role')
        if role == 'admin':
            user.is_superuser = True
        else:
            user.is_superuser = False
        user.save()
    return redirect('user_list')

@login_required
def add_user_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            saved_user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = saved_user
            profile.save()
            messages.success(request, 'Thêm người dùng mới thành công!')
            return redirect('user_profile_list')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'add_edit_user_profile.html', {'user_form': user_form, 'profile_form': profile_form, 'title': 'Thêm thông tin người dùng'})

@login_required
def edit_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Cập nhật người dùng thành công!')
            return redirect('user_profile_list')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'add_edit_user_profile.html', {'user_form': user_form, 'profile_form': profile_form, 'title': 'Chỉnh sửa thông tin người dùng'})

@login_required
def delete_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if hasattr(user, 'profile'):
        user.profile.delete()
    user.delete()
    messages.success(request, 'Xóa người dùng thành công!')
    return redirect('user_profile_list')

# Hotel views
@login_required
def hotel_list(request):
    filter_by = request.GET.get('filter', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')
    
    if filter_by == 'hotel_name':
        if sort_order == 'asc':
            hotels = Hotel.objects.order_by('hotel_name')
        else:
            hotels = Hotel.objects.order_by('-hotel_name')
    else:
        if sort_order == 'asc':
            hotels = Hotel.objects.order_by('created_at')
        else:
            hotels = Hotel.objects.order_by('-created_at')
            
    return render(request, 'hotel_list.html', {'hotels': hotels})

@login_required
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm khách sạn thành công!')
            return redirect('admin_hotels')
    else:
        form = HotelForm()
    return render(request, 'add_edit_hotel.html', {'form': form, 'title': 'Thêm khách sạn mới'})

@login_required
def edit_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sửa khách sạn thành công!')
            return redirect('admin_hotels')
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'add_edit_hotel.html', {'form': form, 'title': 'Sửa khách sạn'})

@login_required
def delete_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        hotel.delete()
        messages.success(request, 'Xóa khách sạn thành công!')
        return redirect('admin_hotels')
    return render(request, 'confirm_delete.html', {'object': hotel, 'title': 'Xóa khách sạn'})

# Room views
@login_required
def room_list(request):
    filter_by = request.GET.get('filter', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if filter_by == 'room_name':
        if sort_order == 'asc':
            rooms = Room.objects.order_by('room_name')
        else:
            rooms = Room.objects.order_by('-room_name')
    else:
        if sort_order == 'asc':
            rooms = Room.objects.order_by('created_at')
        else:
            rooms = Room.objects.order_by('-created_at')
            
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm phòng thành công!')
            return redirect('admin_rooms')
    else:
        form = RoomForm()
    return render(request, 'add_edit_room.html', {'form': form, 'title': 'Thêm phòng mới'})

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sửa phòng thành công!')
            return redirect('admin_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'add_edit_room.html', {'form': form, 'title': 'Sửa phòng'})

@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Xóa phòng thành công!')
        return redirect('admin_rooms')
    return render(request, 'confirm_delete.html', {'object': room, 'title': 'Xóa phòng'})

@login_required
def room_images_list(request):
    filter_by = request.GET.get('filter', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if filter_by == 'room__room_name':
        if sort_order == 'asc':
            images = RoomImages.objects.order_by('room__room_name')
        else:
            images = RoomImages.objects.order_by('-room__room_name')
    else:
        if sort_order == 'asc':
            images = RoomImages.objects.order_by('created_at')
        else:
            images = RoomImages.objects.order_by('-created_at')
            
    return render(request, 'room_image_list.html', {'images': images})

@login_required
def add_room_image(request):
    if request.method == 'POST':
        form = RoomImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm ảnh phòng thành công!')
            return redirect('admin_room_images')
    else:
        form = RoomImageForm()
    return render(request, 'add_edit_room_image.html', {'form': form, 'title': 'Thêm ảnh phòng mới'})

@login_required
def edit_room_image(request, image_id):
    image = get_object_or_404(RoomImages, id=image_id)
    if request.method == 'POST':
        form = RoomImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sửa ảnh phòng thành công!')
            return redirect('admin_room_images')
    else:
        form = RoomImageForm(instance=image)
    return render(request, 'add_edit_room_image.html', {'form': form, 'title': 'Sửa ảnh phòng'})

@login_required
def delete_room_image(request, image_id):
    image = get_object_or_404(RoomImages, id=image_id)
    image.delete()
    messages.success(request, 'Xóa ảnh phòng thành công!')
    return redirect('admin_room_images')

# RoomBooking views
@login_required
def booking_list(request):
    filter_by = request.GET.get('filter', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if filter_by == 'user__user__username':
        filter_by = 'user__user__username'
    elif filter_by == 'payment_status':
        filter_by = 'payment_status'
    elif filter_by == 'booking_status':
        filter_by = 'booking_status'
    else:
        filter_by = 'created_at'

    if sort_order == 'asc':
        bookings = RoomBooking.objects.order_by(filter_by)
    else:
        bookings = RoomBooking.objects.order_by(f'-{filter_by}')
        
    return render(request, 'booking_list.html', {'bookings': bookings})

@login_required
def add_booking(request):
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm đặt phòng thành công!')
            return redirect('admin_bookings')
    else:
        form = RoomBookingForm()
    return render(request, 'add_edit_booking.html', {'form': form, 'title': 'Thêm đặt phòng mới'})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id)
    if request.method == 'POST':
        form = RoomBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sửa đặt phòng thành công!')
            return redirect('admin_bookings')
    else:
        form = RoomBookingForm(instance=booking)
    return render(request, 'add_edit_booking.html', {'form': form, 'title': 'Sửa đặt phòng'})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(RoomBooking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Xóa đặt phòng thành công!')
        return redirect('admin_bookings')
    return render(request, 'confirm_delete.html', {'object': booking, 'title': 'Xóa đặt phòng'})

# Review views
@login_required
def review_list(request):
    filter_by = request.GET.get('filter', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if filter_by == 'user__username':
        filter_by = 'user__username'
    elif filter_by == 'created_at':
        filter_by = 'created_at'
    elif filter_by == 'room__room_name':
        filter_by = 'room__room_name'
    elif filter_by == 'rating':
        filter_by = 'rating'
    else:
        filter_by = 'created_at'

    if sort_order == 'asc':
        reviews = Review.objects.order_by(filter_by)
    else:
        reviews = Review.objects.order_by(f'-{filter_by}')
    return render(request, 'review_list.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm đánh giá thành công!')
            return redirect('admin_reviews')
    else:
        form = ReviewForm()
    return render(request, 'add_edit_review.html', {'form': form, 'title': 'Thêm đánh giá mới'})

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sửa đánh giá thành công!')
            return redirect('admin_reviews')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'add_edit_review.html', {'form': form, 'title': 'Sửa đánh giá'})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Xóa đánh giá thành công!')
        return redirect('admin_reviews')
    return render(request, 'confirm_delete.html', {'object': review, 'title': 'Xóa đánh giá'})


def amenities(request):
    filter_by = request.GET.get('filter', 'created_at')
    sort_order = request.GET.get('sort_order', 'desc')

    if filter_by == 'amenity_name':
        if sort_order == 'asc':
            objs = Amenities.objects.order_by('amenity_name')
        else:
            objs = Amenities.objects.order_by('-amenity_name')
    else:
        if sort_order == 'asc':
            objs = Amenities.objects.order_by('created_at')
        else:
            objs = Amenities.objects.order_by('-created_at')
    return render(request, 'amenity_list.html', {'objs': objs})

@login_required
def add_amenity(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        Amenities.objects.create(amenity_name=name)
        messages.success(request, 'Thêm tiện ích mới thành công!')
        return redirect('admin_amenities')
    
    return render(request, 'add_edit_amenity.html', {'title': 'Thêm tiện ích mới'})

@login_required
def edit_amenity(request, amenity_id):
    amenity = get_object_or_404(Amenities, id=amenity_id)
    
    if request.method == 'POST':
        amenity.name = request.POST.get('name')
        amenity.save()
        
        messages.success(request, 'Sửa tiện ích thành công!')
        return redirect('admin_amenities')
    
    return render(request, 'add_edit_amenity.html', {'title': 'Sửa tiện ích', 'amenity': amenity})

@login_required
def delete_amenity(request, amenity_id):
    amenity = get_object_or_404(Amenities, id=amenity_id)
    amenity.delete()
    messages.success(request, 'Xóa tiện ích thành công!')
    return redirect('admin_amenities')
