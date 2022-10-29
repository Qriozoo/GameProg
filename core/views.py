from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite


@login_required
def dashboard(request):
    #print(User.is_superuser.)
    if request.user.is_superuser:
        #return render(request, '/admin', {})
        return render(request, 'Profile/dashboard.html', {})
    else:
        return render(request, 'Profile/dashboard.html', {})