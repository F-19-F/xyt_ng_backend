from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

# 我们的用户模型

class User(AbstractUser):
    # 学生是0，老师是1
    class IdentityChoice(models.IntegerChoices):
        STUDENT = 0, '学生'
        TEACHER = 1, '老师'
        ADMIN = 2, '管理员'

    # 默认是老师
    identity = models.IntegerField(choices=IdentityChoice.choices, default=IdentityChoice.STUDENT, null=True,
                                   verbose_name="身份")
    name = models.CharField(max_length=50, verbose_name="姓名")
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name="学号/工号",
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    # num = models.CharField(max_length=30,null=True,verbose_name="学号/工号")
    pls = models.CharField(max_length=30, null=True, verbose_name="专业", blank=True)
    cls = models.CharField(max_length=30, null=True, verbose_name="班级", blank=True)
    phone = models.CharField(max_length=20, null=True, verbose_name="手机号", blank=True)

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        name = ""
        if (self.identity == 0):
            name = "学生"
        elif self.identity == 1:
            name = "老师"
        else:
            name = "管理员"
        return f"{name}-{self.name} "


class Course(models.Model):
    # 课程id
    id = models.BigAutoField(primary_key=True, null=False)
    create_teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建老师')
    name = models.CharField(max_length=50, verbose_name="课程名称")
    credit = models.FloatField(verbose_name="课程学分")

    class Meta:
        verbose_name = "课程"

    def __str__(self):
        return f"{self.name}-{self.create_teacher.name}"


class ClassRoom(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    buildingname = models.CharField(max_length=50, verbose_name="教学楼")
    roomname = models.CharField(max_length=50, verbose_name="教室名")

    class Meta:
        verbose_name = "教室"

    def __str__(self):
        return f"{self.buildingname}-{self.roomname}"


class EduClass(models.Model):
    class WeekChoice(models.IntegerChoices):
        Monday = 1, "星期一"
        Tuesday = 2, "星期二"
        Wednesday = 3, "星期三"
        Thursday = 4, "星期四"
        Friday = 5, "星期五"
        Saturday = 6, "星期六"
        Sunday = 7, "星期天"

    class XqChoice(models.IntegerChoices):
        one = 1, "第一学期",
        two = 2, "第二学期"

    id = models.BigAutoField(primary_key=True, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="对应课程")
    week_begin = models.IntegerField(verbose_name="开始周")
    week_end = models.IntegerField(verbose_name="结束周")
    begin_in_day = models.IntegerField(verbose_name="开始节数")
    end_in_day = models.IntegerField(verbose_name="结束节数")
    whichday = models.IntegerField(verbose_name="星期几", choices=WeekChoice.choices)
    xq = models.IntegerField(verbose_name="学期", choices=XqChoice.choices)
    xn = models.IntegerField(verbose_name="学年")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="教学教室")

    class Meta:
        verbose_name = "教学班"

    def __str__(self):
        return f"{self.course.name}-{self.week_begin}->{self.week_end}"


class PeopleClass(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="学生")
    educlass = models.ForeignKey(EduClass, on_delete=models.CASCADE, verbose_name="对应教学班")

    class Meta:
        verbose_name = "教学班人员"


class Work(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    educlass = models.ForeignKey(EduClass, on_delete=models.CASCADE, verbose_name="对应教学班")
    title = models.CharField(max_length=100, verbose_name="作业标题")
    content = models.CharField(max_length=1000, verbose_name="作业要求")

    class Meta:
        verbose_name = "作业"

    def __str__(self):
        return f"{self.educlass}-{self.title}"


class Answer(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name="对应作业")
    people = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作业完成者")
    content = models.CharField(max_length=1000, verbose_name="提交内容")

    class Meta:
        verbose_name = "作业提交"

    def __str__(self):
        return f"{self.people}-{self.work}"


class Exam(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    educlass = models.ForeignKey(EduClass, on_delete=models.CASCADE, verbose_name="对应教学班")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, verbose_name="考试所在教室")
    name = models.CharField(max_length=50, verbose_name="考试名")
    begin_time = models.DateTimeField(verbose_name="考试开始时间")
    end_time = models.DateTimeField(verbose_name="考试结束时间")

    class Meta:
        verbose_name = "考试"

    def __str__(self):
        return f"{self.name}-{str(self.classroom)}"


class Score(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    educlass = models.ForeignKey(EduClass, on_delete=models.CASCADE, verbose_name="对应教学班")
    people = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="对应学生")
    score_normal = models.FloatField(verbose_name="平时分数")
    score_final = models.FloatField(verbose_name="期末分数")
    score = models.FloatField(verbose_name="最终分数")

    class Meta:
        verbose_name = "分数"

    def __str__(self):
        return f"{self.people}-{self.educlass.course.name}-{self.score}"
