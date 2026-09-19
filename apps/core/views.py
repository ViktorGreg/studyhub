from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CafeSettings
from .forms import CafeSettingsForm
from apps.menu.models import MenuCategory

# Create your views here.
def home(request):
  return render(request, 'core/home.html')

def login(request):
  return render(request, 'core/login.html')

@login_required
def dashboard(request):
    settings_obj = CafeSettings.load()

    if request.method == 'POST':
        form = CafeSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved.')
            return redirect('core:dashboard')
    else:
        form = CafeSettingsForm(instance=settings_obj)

    categories = MenuCategory.objects.prefetch_related('items')

    return render(request, 'core/dashboard.html', {
        'form': form,
        'categories': categories,
    })