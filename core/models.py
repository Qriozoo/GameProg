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
    def get_progress_data(user):
        user_exp, user_achievements = Solution.get_user_exp(user)

        base_level_up = 10
        user_lvl = 1
        while True:
            if user_exp >= (base_level_up * user_lvl):
                user_exp -= (base_level_up * user_lvl)
                user_lvl += 1
            else:
                lvl_up_exp = (base_level_up * user_lvl)
                break

        return user_exp, user_lvl, lvl_up_exp, user_achievements
    
    @staticmethod
    def get_user_exp(user):
        user_exp = 0

        user_solutions = Solution.objects.filter(user=user)
        solved_tasks = []
        """"course_stat_dict_template": {
                "sol_num": int,
                "theme_dict": {
                    "pow": int,
                },
                "task_levels": [int_list]
            }"""
        user_stat = {}
        for solution in user_solutions:
            task = Task.objects.get(solutions=solution)
            solved_tasks.append(task)
        for task in solved_tasks:
            user_exp += pow(2, task.level)

            #gather stat info
            if task.course.name not in user_stat.keys():
                user_stat[task.course.name] = {
                    "sol_num": 0,
                    "theme_dict": {},
                    "task_levels": []
                }
            course_stat_dict = user_stat[task.course.name]

            course_stat_dict["sol_num"] = course_stat_dict["sol_num"] + 1

            course_theme_dict = course_stat_dict["theme_dict"]
            for theme in task.themes.all():
                if theme.name not in course_theme_dict.keys():
                    course_theme_dict[theme.name] = 0
                course_theme_dict[theme.name] += 1

            if task.level not in course_stat_dict["task_levels"]:
                course_stat_dict["task_levels"].append(task.level)

        user_achievements = Solution.check_achievements(user_stat)

        for achievement in user_achievements:
            user_exp += pow(2, achievement.level)

        return user_exp, user_achievements
    
    @staticmethod
    def check_achievements(user_stat):
        achievements_list = Achievement.objects.all()
        user_achievements = []
        for achievement in achievements_list:
            achievement_condition = {
                "course_name": achievement.condition.split("\n")[0].split("-")[1].strip(" \r"),
                "min_sol_num": int(achievement.condition.split("\n")[1].split("-")[1].strip(" \r")),
                "themes": achievement.condition.split("\n")[2].split("-")[1].strip(" \r"),
                "task_level": achievement.condition.split("\n")[3].split("-")[1].strip(" \r"),
            }
            cond_theme_dict = {}
            if achievement_condition["themes"] != "Any":
                for theme_data in achievement_condition["themes"].split(","):
                    theme_name = theme_data.split(":")[0].strip(" ")
                    theme_pow = int(theme_data.split(":")[1].strip(" "))
                    cond_theme_dict[theme_name] = theme_pow
            else:
                cond_theme_dict["Any"] = 0
            achievement_condition["themes"] = cond_theme_dict

            if achievement_condition["course_name"] == "Any":
                stat_data = {
                    "sol_num": 0,
                    "theme_dict": {},
                    "task_levels": []
                }
                for course in user_stat:
                    #TODO: Дописать обьединение статистики по курсам
                    pass
            else:
                stat_data = user_stat[achievement_condition["course_name"]]
                
            sol_num_check = stat_data["sol_num"] >= achievement_condition["min_sol_num"]

            for theme in achievement_condition["themes"].keys():
                if theme == "Any":
                    theme_check = True
                    break
                else:
                    if theme in stat_data["theme_dict"].keys():
                        theme_check = stat_data["theme_dict"][theme] >= achievement_condition["themes"][theme]
                    else:
                        theme_check = False
                    if not theme_check:
                            break
            
            if achievement_condition["task_level"] == "Any":
                task_level_check = True
            else:
                task_level_check = int(achievement_condition["task_level"]) in stat_data["task_levels"]

            if sol_num_check and theme_check and task_level_check:
                user_achievements.append(achievement)

        return user_achievements


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


class Achievement(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    condition = models.TextField()

    level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

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