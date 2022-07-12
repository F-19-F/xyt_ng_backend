from django.urls import include, path
from rest_framework import routers
from edubackend import views
router = routers.DefaultRouter()
router.register(r'course',views.CourseViewSet)
router.register(r'educlass',views.EduClassViewSet)
router.register(r'peopleclass',views.PeopleClassViewSet)
router.register(r'work',views.WorkViewSet)
router.register(r'answer',views.AnswerViewSet)
router.register(r'score',views.ScoreViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'exam',views.ExamViewSet)
router.register(r'classroom', views.ClassRoomViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # restful接口
    path('', include(router.urls)),
    # csrf防护接口
    path('getCsrftoken/',views.getCsrfToken),
    # 登录接口
    path('auth/', include('dj_rest_auth.urls')),
]