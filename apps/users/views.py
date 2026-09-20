from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
from .forms import StaffForm


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return HttpResponseForbidden("Only admins can do that.")
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(request, username=username, password=password)

        if account is not None:
            login(request, account)
            return redirect('core:dashboard')
        else:
            return render(request, 'core/login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'core/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required
def profile(request):
    return render(request, 'users/profile.html', {
        'target_user': request.user,
        'is_own_profile': True,
        'can_edit_password': request.user.role == 'ADMIN',
    })


@login_required
@admin_required
def staff_detail(request, staff_id):
    staff = get_object_or_404(Account, pk=staff_id, role='STAFF')
    return render(request, 'users/profile.html', {
        'target_user': staff,
        'is_own_profile': False,
        'can_edit_password': True,
    })


@login_required
@admin_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff account created.')
        else:
            messages.error(request, f"Couldn't add staff: {form.errors}")
    return redirect('core:dashboard')

@login_required
@admin_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(Account, pk=staff_id, role='STAFF')
    if request.method == 'POST':
        staff.delete()
        messages.success(request, f'{staff.first_name} {staff.last_name} removed.')
    return redirect('core:dashboard')