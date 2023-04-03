from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.utils import timezone


class Course(models.Model):    
    name = models.CharField(max_length=50)
    description = models.TextField()

    def subscribe_student(self, user):
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            student = Student.objects.create(user=user)
        student.courses.add(self)

    def __str__(self):
        return self.name
    

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)


class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Solution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)

    def save_solution(self, tpk, user):
        solution = Solution.objects.create(
            user=user,
            date=timezone.now(),
            text=self.text,
            )
        task = Task.objects.get(pk=tpk)
        task.solutions.add(solution)

    @staticmethod
    def get_lvl_data(user):
        user_exp = 0

        user_solutions = Solution.objects.filter(user=user)
        solved_tasks = []
        for solution in user_solutions:
            task = Task.objects.get(solutions=solution)
            solved_tasks.append(task)
        for task in solved_tasks:
            user_exp += pow(2, task.level)

        base_level_up = 10
        user_lvl = 1
        while True:
            if user_exp >= (base_level_up * user_lvl):
                user_exp -= (base_level_up * user_lvl)
                user_lvl += 1
            else:
                lvl_up_exp = (base_level_up * user_lvl)
                break
        return user_exp, user_lvl, lvl_up_exp


class Task(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    themes = models.ManyToManyField(Theme)
    name = models.CharField(max_length=30)

    text = models.TextField()
    test = models.TextField()

    level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    solutions = models.ManyToManyField(Solution, blank=True, unique=False)

    def __str__(self):
        return self.name


"""class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_name = models.TextField()
    first_name = models.TextField()
    #courses = models.ManyToManyField("Course", blank=True)

    class Meta:
        verbose_name_plural = "Students"""

"""class Course(models.Model):
    name = models.TextField()
    year = models.IntegerField()

    class Meta:
        unique_together = ("name", "year", )

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    course = models.ForeignKey(Course, on_delete=models.CASCADE)"""