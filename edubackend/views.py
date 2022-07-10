import django
import rest_framework.response
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import JsonResponse
from datetime import datetime, timezone, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# rest_framework url过滤
from django_filters.rest_framework import DjangoFilterBackend
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

    @action(detail=False)
    def getcoursebyme(self,request:Request,*args,**kwargs):
        user = self.request.user
        # 学生无权限获取
        if user.identity != User.IdentityChoice.TEACHER:
            raise ValidationError(detail="非老师无法获取")
        # res = []
        objs = Course.objects.filter(create_teacher=user)
        r = CourseSerializer(objs,many=True)
        return Response(r.data)



class EduClassViewSet(viewsets.ModelViewSet):
    queryset = EduClass.objects.all()
    serializer_class = EduClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course','xq','xn']

    @action(detail=False)
    def courseselect(self, request: Request, *args, **kwargs):
        try:
            xqm = int(request.query_params['xqm'])
            xnm = int(request.query_params['xnm'])
        except MultiValueDictKeyError:
            return Response({}, status=404)
        except Exception as e:
            return Response({}, status=404)

        if xqm and xnm:
            objs = EduClass.objects.filter(xq=xqm, xn=xnm)
        else:
            return Response([])
        res = []
        for educlass in objs:
            peopleclass_set = educlass.peopleclass_set.filter(student=self.request.user)
            selected = False
            peopleid = -1
            if len(peopleclass_set) > 0:
                selected = True
                peopleid = peopleclass_set.all()[0].id
            res.append({
                "jxb_id": educlass.pk,
                "kc": educlass.course.name,
                "xf": educlass.course.credit,
                "loc": str(educlass.classroom),
                "teacher": educlass.course.create_teacher.name,
                "selected": selected,
                "pcs_id":peopleid
            })
        # res= [{
        #     "jxb_id":educlass.pk,
        #     "kc":educlass.course.name,
        #     "xf":educlass.course.credit,
        #     "loc":str(educlass.classroom),
        #     "teacher":educlass.course.create_teacher.name,
        #     "selected":True if len(educlass.peopleclass_set.filter(student=self.request.user)) >0 else False
        # }for educlass in objs]

        return Response(res)


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
            begin = begin + self.td_bj
            if begin < now:
                continue
            res.append({
                "kcmc": exam.educlass.course.name,
                "kssj": begin.strftime("%Y-%m-%d %H:%M"),
                "rday": (begin - now).days,
                "cdbh": str(exam.classroom)
            })
        return Response(res)


class PeopleClassViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    queryset = PeopleClass.objects.all()
    serializer_class = PeopleClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['educlass']


    def create(self, request, *args, **kwargs):
        user = self.request.user
        try:
            uid = int(request.data['student'])
            eid = int(request.data['educlass'])
        except:
            raise ValidationError(detail="参数错误")
        # 只允许本用户添加属于自己课程
        if (uid != user.id):
            raise ValidationError(detail="不允许代替选课!")
        exist_objs = PeopleClass.objects.filter(student=user, educlass__id=eid)
        if len(exist_objs) > 0:
            raise ValidationError(detail="你已经选过这门课了，不可以重复选课")
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        ins = self.get_object()
        # ins = PeopleClass()
        if ins.student.id != user.id and user.identity == User.IdentityChoice.STUDENT:
            raise ValidationError(detail="禁止删除不属于你的课程")
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.identity==User.IdentityChoice.STUDENT:
            objs = PeopleClass.objects.filter(student=user)
        else:
            objs = PeopleClass.objects.filter(educlass__course__create_teacher=user)

        return objs


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    @action(detail=False)
    def mywork(self,request,*args,**kwargs):
        objs = self.get_queryset()
        res  = []
        for work in objs:
            res.append({
                "id":work.pk,
                "title":work.title,
                "from":work.educlass.course.name,
                "deadline":"截止时间"
            } )
        return Response(res)


    def get_queryset(self):
        user = self.request.user
        if user.identity == User.IdentityChoice.STUDENT or user.identity == User.IdentityChoice.ADMIN:
            objs = Work.objects.filter(educlass__peopleclass__student=user)
        else:
            objs = Work.objects.filter(educlass__course__create_teacher=user)
        return objs



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends =  [DjangoFilterBackend]
    filterset_fields = ['work']
    def create(self, request, *args, **kwargs):
        user = self.request.user
        try:
            uid = int(request.data['people'])
            wid = int(request.data['work'])
        except:
            raise ValidationError(detail="参数错误")
        # 只允许本用户添加属于自己课程
        if (uid != user.id):
            raise ValidationError(detail="不允许代替提交作业")
        exist_objs =  Answer.objects.filter(people=user,work__id=wid)
        if len(exist_objs) > 0:
            raise ValidationError(detail="你已经提交过作业了,不能重复提交!")
        return super().create(request, *args, **kwargs)


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
