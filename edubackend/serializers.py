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



# class userStudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = userStudents
#         fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups','name','identity']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
