from django.contrib.auth.models import User, Group
from .models import userStudents
from rest_framework import serializers


class userStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = userStudents
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
