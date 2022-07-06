from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
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


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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
