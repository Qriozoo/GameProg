import random

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite

from .models import Course, Student, Task, Solution, Achievement
from .forms import SolutionForm
from .executor import test_script


@login_required
def dashboard(request):
    user_exp, user_lvl, lvl_up_exp, user_achievements = Solution.get_progress_data(user=request.user)

    achievements_list = Achievement.objects.all()
    locked_achievements = []
    for achievement in achievements_list:
        if achievement not in user_achievements:
            locked_achievements.append(achievement)

    try:
        user_courses = Student.objects.get(user=request.user).courses.all()
    except Student.DoesNotExist:
        user_courses = []

    return render(request, 'profile/dashboard.html', {
        'user_courses': user_courses,
        'user_exp': user_exp,
        'user_lvl': user_lvl,
        'lvl_up_exp': lvl_up_exp,
        'user_achievements': user_achievements,
        'locked_achievements': locked_achievements})

@login_required
def top_list(request):
    students = Student.objects.all()

    user_list = []
    for student in students:
        user_list.append(student.user)

    user_dict = {}
    for user in user_list:
        user_exp, user_lvl, lvl_up_exp, user_achievements = Solution.get_progress_data(user=user)
        all_exp = 10 * (user_lvl - 1) + user_exp
        user_dict[all_exp] = '%s    level:%s exp:%s/%s\n achievements:%s' % (
            user.username,
            user_lvl,
            user_exp,
            lvl_up_exp,
            len(user_achievements)
            )
    user_dict_sorted = dict(sorted(user_dict.items(), reverse=True))
    
    user_lvl_info = []
    num = 1
    for key in user_dict_sorted:
        user_lvl_info.append('%s: %s' % (num, user_dict_sorted[key]))
        num += 1

    return render(request, 'profile/top.html', {'user_lvl_info': user_lvl_info})
    
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
    themes = ""

    if len(course_tasks) != 0:
        task_list = []
        for task in list(course_tasks):
            task_list.append(task)
        rc = True
        while rc:
            if task_list != []:
                rand_task = task_list.pop(random.randint(0, len(task_list) - 1))
                s_user_list = []
                for solution in rand_task.solutions.all():
                    s_user_list.append(solution.user)
                if request.user not in s_user_list:
                    task = rand_task
                    for theme in task.themes.all():
                        themes += "%s " % theme
                    rc = False
            else:
                task = False
                break
    else:
        task = False
    return render(request, 'course/course_workout.html', {'course': course, 'task': task, 'themes': themes})

@login_required
def task_train(request, cpk, tpk):
    course = get_object_or_404(Course, pk=cpk)
    task = get_object_or_404(Task, pk=tpk)

    themes = ""
    for theme in task.themes.all():
        themes += "%s " % theme

    if request.method == "POST" and 'Test' in request.POST:
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            result = test_script(solution.text, task.test)
            return render(
                request,
                'course/task_train.html',
                {'course': course,
                 'task': task,
                 'themes': themes,
                 'form': form,
                 'result': result}
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
                return render(
                    request,
                    'course/task_train.html',
                    {'course': course,
                     'task': task,
                     'themes': themes,
                     'form': form,
                     'result': result}
                    )
    else:
        form = SolutionForm()

    return render(
        request,
        'course/task_train.html',
        {'course': course,
        'task': task,
        'themes': themes,
        'form': form
        })

@login_required
def task_solutions(request, cpk, tpk):
    course = get_object_or_404(Course, pk=cpk)
    task = get_object_or_404(Task, pk=tpk)

    themes = ""
    for theme in task.themes.all():
        themes += "%s " % theme

    solutions = []
    for solution in task.solutions.all():
        solutions.append(solution)

    return render(request,'course/task_solutions.html', {
        'course': course,
        'task': task,
        'themes': themes,
        'solutions': solutions
        })

@login_required
def course_subscribe(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.subscribe_student(request.user)
    return redirect('course_detail', pk=pk)