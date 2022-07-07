from django.contrib.auth.models import Group
from rest_framework import serializers

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


class CourseSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance:Course):
    #     origin=  super(CourseSerializer, self).to_representation(instance)
    #     # zcd = [i for i in range(instance.educlass.week_begin,instance.educlass.week_end + 1)]
    #     extend_info = {
    #         # 'kcmc': instance.name,
    #         # 'cdmc': '默认地点',
    #         'xm': instance.create_teacher.name,
    #         # 'zcdd': len(zcd),
    #         # 'zcd': zcd,
    #         # "xqj": instance.educlass.whichday,
    #         # 'jcs': instance.educlass.begin_in_day,
    #         # 'cxjs': instance.educlass.end_in_day - instance.educlass.begin_in_day,
    #         "xf": instance.credit,
    #         'bg': 'blue'
    #     }
    #     origin.update(extend_info)
    #     return origin
    class Meta:
        model = Course
        fields = '__all__'


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
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
        fields = ['url', 'username', 'email', 'groups', 'name', 'identity', 'pls', 'cls']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
