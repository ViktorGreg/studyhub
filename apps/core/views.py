from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CafeSettings
from .forms import CafeSettingsForm
from apps.menu.models import MenuCategory
from apps.users.models import Account
from apps.studyhub.models import StudyHubSettings, StudyHubPlan, Booking, Session

# Create your views here.
def home(request):
  return render(request, 'core/home.html', {
    'plans': StudyHubPlan.objects.all(),
    'settings': CafeSettings.load(),
    'categories': MenuCategory.objects.prefetch_related('items'),
  })

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

    studyhub_settings = StudyHubSettings.load()
    categories = MenuCategory.objects.prefetch_related('items')
    plans = StudyHubPlan.objects.all()
    for plan in plans:
        plan.active_bookings = (
            Booking.objects
            .filter(plan=plan, status="ACTIVE")
            .prefetch_related("sessions")
        )
    bookings = Booking.objects.prefetch_related('sessions')
    staff_list = Account.objects.filter(role='STAFF')

    return render(request, 'core/dashboard.html', {
        'studyhub_settings': studyhub_settings,
        'form': form,
        'plans': plans,
        'categories': categories,
        'bookings': bookings,
        'staff_list': staff_list,
    })