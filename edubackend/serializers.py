from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import (
    User,
    Course,
    EduClass,
    PeopleClass,
    Work,
    Answer,
    Score
)


class CourseSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance:Course):
    #     origin=  super(CourseSerializer, self).to_representation(instance)
    #     origin["xm"] = instance.create_teacher.name
    #     origin["xf"] = instance.credit
    #     return origin
    class Meta:
        model = Course
        fields = '__all__'


class EduClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = EduClass
        fields = '__all__'


class PeopleClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleClass
        fields = '__all__'


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'name', 'identity','pls','cls']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
