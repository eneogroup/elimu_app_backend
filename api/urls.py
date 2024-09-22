from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.account_view import TeacherSchoolViewSet
from api.views.auth.authentication_api import LoginAPIView, LogoutAPIView
from rest_framework.routers import DefaultRouter
from .views.admin_manager.admin_manager_views import *
from .views.school_manager.school_manager_view import (
    SchoolYearViewSet, ClassroomViewSet
)

router = DefaultRouter()

# URL FOR ACCOUNT
router.register(r'teachers-school', TeacherSchoolViewSet, basename='teachers-school')

# URL FOR SCHOOL MANAGER
router.register(r'school-years', SchoolYearViewSet, basename='schoolyear')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
# URL FOR ADMIN MANAGER
router.register(r'school-cycles', SchoolCycleViewSet, basename='schoolcycle')
router.register(r'school-series', SchoolSeriesViewSet, basename='schoolseries')
router.register(r'school-levels', SchoolLevelViewSet, basename='schoollevel')
router.register(r'subject-groups', SubjectGroupViewSet, basename='subjectgroup')
router.register(r'document-types', DocumentTypeViewSet, basename='documenttype')
router.register(r'sanction-appreciation-types', SanctionOrAppreciationTypeViewSet, basename='sanctionappreciationtype')


urlpatterns = [
    path('', include(router.urls)),
    #URL FOR AUTHENTICATION
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
