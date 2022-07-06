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
import  dj_rest_auth
# router.register(r'users', views.userStudentViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('getCsrftoken/',views.getCsrfToken),
    path('auth/', include('dj_rest_auth.urls')),
]