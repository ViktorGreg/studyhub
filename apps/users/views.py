from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


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