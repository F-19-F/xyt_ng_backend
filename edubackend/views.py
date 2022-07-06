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
from edubackend.serializers import (
    UserSerializer,
    GroupSerializer,
    CourseSerializer,
    EduClassSerializer,
    PeopleClassSerializer,
    WorkSerializer,
    AnswerSerializer,
    ScoreSerializer
)
from .models import (
    User,
    Course,
    EduClass,
    PeopleClass,
    Work,
    Answer,
    Score
)

def getCsrfToken(request):
    res = {
        'csrftoken':django.middleware.csrf.get_token(request)
    }
    return JsonResponse(res)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    @action(detail=True)
    def getDetail(self,request:Request,*args,**kwargs):
        Obj = self.get_object()
        # request.user.identity
        res={}
        # Obj = Course()
        # EduClass.objects.filter()
        res["xm"] = Obj.create_teacher.name
        # res[""]
        return  Response(res)


class EduClassViewSet(viewsets.ModelViewSet):
    queryset = EduClass.objects.all()
    serializer_class = EduClassSerializer


class PeopleClassViewSet(viewsets.ModelViewSet):
    queryset = PeopleClass.objects.all()
    serializer_class = PeopleClassSerializer


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


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
