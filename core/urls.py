from django.shortcuts import redirect
from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/')),
    path('dashboard/', views.dashboard, name='dashboard'),
]