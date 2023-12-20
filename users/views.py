from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from users.form import LoginForm


# from .forms import LoginForm
# Create your views here.


def login_page(request):
    error_message = None
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Kullanıcı adı veya şifre hatalı!"

    context = {'form': forms, 'error_message': error_message}
    return render(request, 'users/sistem.html', context)


def logout_page(request):
    logout(request)
    return redirect('sistem')


def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Gönderilecek e-posta bilgileri
        send_mail(
            subject,
            message,
            email,  # Gönderici e-posta
            ['k.metin01@gmail.com'],  # Alıcı e-posta
            fail_silently=False,
        )

        # E-posta gönderildikten sonra başka bir sayfaya yönlendirme
        return HttpResponseRedirect('/success/')  # Başarılı sayfası

    return render(request, 'users/contact.html')
