import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite

from .models import Course, Student, Theme, Task
from .forms import SolutionForm
from .executor import test_script


@login_required
def dashboard(request):
    #print(User.is_superuser.)
    try:
        user_courses = Student.objects.get(user=request.user).courses.all()
    except Student.DoesNotExist:
        user_courses = []
    if request.user.is_superuser:
        #return render(request, '/admin', {})
        return render(request, 'Profile/dashboard.html', {'user_courses': user_courses})
    else:
        return render(request, 'Profile/dashboard.html', {'user_courses': user_courses})
    
def course_list(request):
    """posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})"""
    courses = Course.objects.order_by('name')
    return render(request, 'course/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    try:
        user_courses = Student.objects.get(user=request.user).courses.all()
    except Student.DoesNotExist:
        user_courses = []
    subscribed =  True if course in user_courses else False
    return render(request, 'course/course_detail.html', {'course': course, 'subscribed': subscribed})

@login_required
def course_workout(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_tasks = Task.objects.filter(course=course)
    
    if len(course_tasks) != 0:
        task = course_tasks[random.randint(0, len(course_tasks) - 1)]
    else:
        task = False
    return render(request, 'course/course_workout.html', {'course': course, 'task': task})

@login_required
def task_train(request, cpk, tpk):
    course = get_object_or_404(Course, pk=cpk)
    task = get_object_or_404(Task, pk=tpk)

    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            test_script(solution.text, task.test)
            #post.author = request.user
            #post.save()
            #return redirect('post_detail', pk=post.pk)
            return render(request, 'course/task_train.html', {'course': course, 'task': task, 'form': form})
    else:
        form = SolutionForm()

    return render(request, 'course/task_train.html', {'course': course, 'task': task, 'form': form})

@login_required
def course_subscribe(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.subscribe_student(request.user)
    return redirect('course_detail', pk=pk)