from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    themes = models.ManyToManyField(Theme)
    name = models.CharField(max_length=30)
    text = models.TextField()
    test = models.TextField()

    def __str__(self):
        return self.name


class Solution(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()


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