import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite

from .models import Course, Student, Task, Solution
from .forms import SolutionForm
from .executor import test_script


@login_required
def dashboard(request):
    user_exp, user_lvl, lvl_up_exp = Solution.get_lvl_data(user=request.user)

    try:
        user_courses = Student.objects.get(user=request.user).courses.all()
    except Student.DoesNotExist:
        user_courses = []

    return render(request, 'Profile/dashboard.html', {
        'user_courses': user_courses,
        'user_exp': user_exp,
        'user_lvl': user_lvl,
        'lvl_up_exp': lvl_up_exp})

@login_required
def top_list(request):
    user_list = Student.objects.get().user

    user_dict = {}
    for user in (user_list,):
        user_exp, user_lvl, lvl_up_exp = Solution.get_lvl_data(user=user)
        user_dict[user_exp] = '%s    level:%s exp:%s/%s' % (user.username, user_lvl, user_exp, lvl_up_exp)
    user_dict_sorted = dict(sorted(user_dict.items()))
    
    user_lvl_info = []
    num = 1
    for key in user_dict_sorted:
        user_lvl_info.append('%s: %s' % (num, user_dict_sorted[key]))
        num += 1


    """user_lvl_info = []
    for user in (user_list,):
        user_exp, user_lvl, lvl_up_exp = Solution.get_lvl_data(user=user)
        user_lvl_info.append('%s    level:%s exp:%s/%s' % (user.username, user_lvl, user_exp, lvl_up_exp))"""

    return render(request, 'Profile/top.html', {'user_lvl_info': user_lvl_info})
    
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
    if request.method == "POST" and 'Test' in request.POST:
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            result = test_script(solution.text, task.test)
            return render(
                request,
                'course/task_train.html',
                {'course': course, 'task': task, 'form': form, 'result': result}
                )
    elif request.method == "POST" and 'Save' in request.POST:
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            result = test_script(solution.text, task.test)
            test_passed = True
            for test in result:
                if 'False' in test:
                    test_passed = False
                    break
            if test_passed:
                solution.save_solution(task.pk, request.user)
                return redirect(
                    'task_solutions',
                    cpk=course.pk,
                    tpk=task.pk
                    )
            else:
                #post.author = request.user
                #post.save()
                #return redirect('post_detail', pk=post.pk)
                return render(
                    request,
                    'course/task_train.html',
                    {'course': course, 'task': task, 'form': form, 'result': result}
                    )
    else:
        form = SolutionForm()

    return render(request, 'course/task_train.html', {'course': course, 'task': task, 'form': form})

@login_required
def task_solutions(request, cpk, tpk):
    course = get_object_or_404(Course, pk=cpk)
    task = get_object_or_404(Task, pk=tpk)

    print(task.solutions.all())
    solutions = []
    for solution in task.solutions.all():
        solutions.append(solution)

    return render(request,'course/task_solutions.html', {
        'course': course,
        'task': task,
        'solutions': solutions
        })

@login_required
def course_subscribe(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.subscribe_student(request.user)
    return redirect('course_detail', pk=pk)