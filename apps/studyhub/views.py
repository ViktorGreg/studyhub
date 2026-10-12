from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking, StudyHubSettings, Session
from apps.users.models import Account
from .forms import BookingForm, SessionForm, SettingsForm
from django.utils import timezone


def create_booking(request):
  if request.method != 'POST':
    return JsonResponse({'success': False}, status=405)

  settings_obj = StudyHubSettings.load()
  active_count = Booking.objects.filter(status='ACTIVE').count()

  if active_count >= settings_obj.max_capacity:
    return JsonResponse({
      'success': False,
      'errors': {'capacity': ['Study hub is currently full. Please try again later.']}
    }, status=400)

  form = BookingForm(request.POST)
  if form.is_valid():
    booking = form.save()
    return JsonResponse({
      'success': True,
      'booking': {
        'code': booking.booking_code,
        'guest_name': booking.guest_name,
        'plan_name': booking.plan.name,
        'duration_hours': booking.duration_hours,
      }
    })
  return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
def start_session(request):
  if request.method != 'POST':
    return JsonResponse({'success': False}, status=405)

  settings_obj = StudyHubSettings.load()
  active_count = Booking.objects.filter(status='ACTIVE').count()

  if active_count >= settings_obj.max_capacity:
    messages.error(request, 'Study hub is currently full. Please try again later.')
    return redirect('core:dashboard')

  form = SessionForm(request.POST)
  if form.is_valid():
    session = form.save(commit=False)
    if not Session.objects.filter(booking_id=session.booking_id).exists():

      session.started_by = request.user
      session.started_at = timezone.now()
      session.save()

      Booking.objects.filter(id=session.booking_id).update(status = "ACTIVE")

      messages.success(request, 'Session started.')
      return redirect('core:dashboard')
    else:
      messages.error(request, 'Session for this booking is already active.')
      return redirect('core:dashboard')
  else:
    messages.error(request, 'Could not start session.')
  return redirect('core:dashboard')

@login_required
def finish_session(request):
  if request.method != 'POST':
    return JsonResponse({'success': False}, status=405)

  form = SessionForm(request.POST)
  if form.is_valid():
    session = form.save(commit=False)
    if Session.objects.filter(booking_id=session.booking_id).exists():

      session.ended_by = request.user
      session.ended_at = timezone.now()
      session.save()
      
      Booking.objects.filter(id=session.booking_id).update(status = "COMPLETED")

      messages.success(request, 'Session finished.')
      return redirect('core:dashboard')
    else:
      messages.error(request, 'Session for this booking did not start yet or is already finished.')
      return redirect('core:dashboard')
  else:
    messages.error(request, 'Could not finish session.')
  return redirect('core:dashboard')

@login_required
def update_settings(request):
  if request.method != 'POST':
    return JsonResponse({'success': False}, status=405)

  settings_obj = StudyHubSettings.load()
  active_count = Booking.objects.filter(status='ACTIVE').count()

  if active_count >= settings_obj.max_capacity:
    messages.error(request, 'Study hub is currently full. Please try again later.')
    return redirect('core:dashboard')

  form = SettingsForm(request.POST)
  if form.is_valid():
    settings = form.save(commit=False)
    settings.save()

  else:
    messages.error(request, 'Could not update settings.')
  return redirect('core:dashboard')
