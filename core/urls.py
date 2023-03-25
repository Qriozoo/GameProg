from django.shortcuts import redirect
from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/workout/<int:pk>', views.course_workout, name='course_workout'),
    path('course/workout/<int:cpk>/train/<int:tpk>', views.task_train, name="task_train"),
    path('course/workout/<int:cpk>/train/<int:tpk>/solutions', views.task_solutions, name="task_solutions"),
    path('course/<int:pk>/subscribe/', views.course_subscribe, name='course_subscribe'),
]