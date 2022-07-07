import django
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import JsonResponse
from datetime import datetime,timezone,timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from edubackend.serializers import (
    UserSerializer,
    GroupSerializer,
    CourseSerializer,
    EduClassSerializer,
    PeopleClassSerializer,
    WorkSerializer,
    AnswerSerializer,
    ScoreSerializer,
    ClassRoomSerializer,
    ExamSerializer
)
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

def getCsrfToken(request):
    res = {
        'csrftoken': django.middleware.csrf.get_token(request)
    }
    return JsonResponse(res)




class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    # 限制
    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return Course.objects.all()
    #     return Course.objects.filter(self.request.user)


    @action(detail=False)
    def mycourse(self, request: Request, *args, **kwargs):
        user = self.request.user
        myclass = PeopleClass.objects.filter(student=user)
        res = []
        for cls in myclass:
            meduclass = cls.educlass
            mcourse = meduclass.course
            zcd = [i for i in range(meduclass.week_begin, meduclass.week_end + 1)]
            course = {
                'kcmc': mcourse.name,
                'cdmc': str(meduclass.classroom),
                'xm': mcourse.create_teacher.name,
                'zcdd': len(zcd),
                'zcd': zcd,
                "xqj": meduclass.whichday,
                'jcs': meduclass.begin_in_day,
                'cxjs': meduclass.end_in_day - meduclass.begin_in_day,
                'bg': 'blue'
            }
            res.append(course)
        return Response(res)


class EduClassViewSet(viewsets.ModelViewSet):
    queryset = EduClass.objects.all()
    serializer_class = EduClassSerializer


class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    td_bj = timedelta(hours=8)
    @action(detail=False)
    def myexam(self, request: Request, *args, **kwargs):
        user = self.request.user
        exams = Exam.objects.filter(educlass__peopleclass__student=user)
        now = datetime.utcnow() + self.td_bj
        res = []
        for exam in exams:
            # 硬编码了
            begin = datetime.utcfromtimestamp(exam.begin_time.timestamp())
            begin = begin+self.td_bj
            if begin < now :
                continue
            res.append({
                "kcmc":exam.educlass.course.name,
                "kssj":begin.strftime("%Y-%m-%d %H:%M"),
                "rday":(begin - now).days,
                "cdbh":str(exam.classroom)
        })
        return Response(res)



class PeopleClassViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = PeopleClass.objects.all()
    serializer_class = PeopleClassSerializer

    def get_queryset(self):
        user = self.request.user
        # print(user)
        objs = PeopleClass.objects.filter(student=user)
        # print(objs)
        return objs


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    @action(detail=False)
    def myscore(self, request: Request, *args, **kwargs):
        user = self.request.user
        myscore = Score.objects.filter(educlass__peopleclass__student=user)
        res = [{
            "kc": score.educlass.course.name,
            "xf": score.educlass.course.credit,
            "jd": 0 if score.score < 60 else (score.score - 50) / 10,
            "jxb_id": score.educlass.pk,
            "cj": score.score,
        } for score in myscore]
        return Response(res)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
