from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse

admin.site.site_title = "校园通-NG后台"
admin.site.site_header = "校园通-NG后台"
admin.site.index_header = "校园通管理"

from .models import (
    User,
    Course,
    EduClass,
    PeopleClass,
    Work,
    Answer,
    Score,
    ClassRoom,
    Exam
)


# admin.site.register(User, UserAdmin)
@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ("username", "name", "phone","pls", "cls", "identity",)
    list_editable = ("name", "pls", "cls", "phone")
    list_filter = ("identity", "is_superuser")
    search_fields = ("name", "username")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "name", "identity", "password1", "password2"),
            },
        ),
    )


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    # Course.credit
    list_display = ('name', 'create_teacher', 'credit')


@admin.register(EduClass)
class EduClassModelAdmin(admin.ModelAdmin):
    # EduClass.
    list_display = ('course', 'whichday', 'begin_in_day', 'end_in_day','classroom')


@admin.register(PeopleClass)
class PeopleClassModelAdmin(admin.ModelAdmin):
    list_display = ('educlass', 'student')


@admin.register(Work)
class WorkModelAdmin(admin.ModelAdmin):
    # Work.
    list_display = ('educlass', 'title')


@admin.register(Answer)
class AnswerModelAdmin(admin.ModelAdmin):
    # Answer.
    list_display = ('people', 'work', 'content')


@admin.register(Score)
class ScoreModelAdmin(admin.ModelAdmin):
    # Score.
    list_display = ('people', 'score', 'educlass')


@admin.register(ClassRoom)
class ClassRoomModelAdmin(admin.ModelAdmin):
    list_display = ("buildingname", "roomname")


@admin.register(Exam)
class ExamModelAdmin(admin.ModelAdmin):
    # Exam.classroom
    list_display = ("educlass", "name","classroom" ,"begin_time", "end_time")
