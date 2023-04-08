from django.contrib import admin
from .models import Course, Theme, Task, Achievement


admin.site.register(Course)
admin.site.register(Theme)
admin.site.register(Task)
admin.site.register(Achievement)