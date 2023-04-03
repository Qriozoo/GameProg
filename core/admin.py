from django.contrib import admin
from .models import Course, Theme, Task 


admin.site.register(Course)
admin.site.register(Theme)

class TaskAdmin(admin.ModelAdmin):
    exclude = ["Solutions"]

admin.site.register(Task)