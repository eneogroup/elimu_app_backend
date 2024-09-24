from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.account_view import ParentOfStudentViewSet, PupilViewSet, TeacherSchoolViewSet
from api.views.auth.authentication_api import LoginAPIView, LogoutAPIView
from rest_framework.routers import DefaultRouter
from api.views.school_manager.subject_manager_view import SchoolCalendarViewSet, SchoolHolidayViewSet, SchoolProgramViewSet, SchoolScheduleViewSet
from .views.admin_manager.admin_manager_views import *
from .views.school_manager.school_manager_view import (
    InscriptionViewSet, SchoolYearViewSet, ClassroomViewSet, StudentEvaluationViewSet
)

router = DefaultRouter()

# URL FOR ACCOUNT
router.register(r'teachers-school', TeacherSchoolViewSet, basename='teachers-school')
router.register(r'parents', ParentOfStudentViewSet, basename='parents')
router.register(r'pupils', PupilViewSet, basename='pupils')

# URL FOR SCHOOL MANAGER
router.register(r'school-years', SchoolYearViewSet, basename='schoolyear')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'inscriptions', InscriptionViewSet, basename="inscriptions")
router.register(r'student-evaluations', StudentEvaluationViewSet, basename="student-evaluations")

#URL FOR SUBJECT MANAGER
router.register(r'school-calendars', SchoolCalendarViewSet, basename='schoolcalendar')
router.register(r'school-holidays', SchoolHolidayViewSet, basename='schoolholiday')
router.register(r'school-programs', SchoolProgramViewSet, basename='schoolprogram')
router.register(r'school-schedules', SchoolScheduleViewSet, basename='schoolschedule')

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
