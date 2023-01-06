from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def login_form(request):
    context = {}
    if settings.DEBUG:
        if 'du' in request.GET:
            try:
                user = User.objects.get_by_natural_key(request.GET['du'])
                login(request, user)
                return redirect(request.GET['next'])
            except User.DoesNotExist:
                return redirect('login')
        context['dev_accounts'] = User.objects.all()
    return render(request, 'login/login.html', context)
