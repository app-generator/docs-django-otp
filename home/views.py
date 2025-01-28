import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.forms import OtpEmailForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout
from django.urls import reverse
from home.models import OTP

# Create your views here.

from .models import *

@login_required(login_url='/login/')
def index(request):
  context = {}
  return render(request, 'index.html', context)

def otp_login(request):
  form = OtpEmailForm()

  if request.method == 'POST':
    form = OtpEmailForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email')
      user = User.objects.filter(email=email).first()
      if user:
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OTP.objects.update_or_create(user=user, defaults={'otp':otp_code})
        otp_link = request.build_absolute_uri(reverse('validate_otp', args=[otp_code]))

        # Send lgoin link via email
        send_mail(
          'Your Login Link',
          f'Click the link to log in: {otp_link}',
          settings.EMAIL_HOST_USER,
          [email],
          fail_silently=False,
        )

        return render(request, 'login.html', {
          'form': form, 
          'success': 'An email send to your mail.'
        })


  return render(request, 'login.html', {'form': form})


def validate_otp(request, code):
  try:
    otp = OTP.objects.get(otp=code)
    if otp.user:
      login(request, otp.user)
      otp.delete()
      return redirect('/')
  except OTP.DoesNotExist:
    print("Invalid OTP")

  return render(request, 'validate.html', {'error': 'Invalid or expired login link.'})


@login_required(login_url='/login/')
def logout_view(request):
  logout(request)
  return redirect(reverse('otp_login'))