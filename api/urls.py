from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.account_view import CurrentUserViewSet, ParentOfStudentViewSet, PasswordResetConfirmView, PasswordResetView, TeacherSchoolViewSet, UserViewSet
from api.views.auth.authentication_api import LoginAPIView, LogoutAPIView
from rest_framework.routers import DefaultRouter
from api.views.communication_view import AnnouncementViewSet, EventViewSet, InformationViewSet, TagViewSet
from api.views.library_view import EbookViewSet
from api.views.subject_manager_view import SchoolCalendarViewSet, SchoolHolidayViewSet, SchoolProgramViewSet, SchoolScheduleViewSet, SubjectAttributionViewSet
from .views.admin_manager_views import *
from .views.school_manager_view import (
    ActiveSchoolYearStudentsView, ActiveSchoolYearViewSet, InscriptionViewSet, SchoolStatisticsView, SchoolYearViewSet, ClassroomViewSet, StudentEvaluationViewSet
)

router = DefaultRouter()

# URL FOR ACCOUNT
router.register(r'teachers-school', TeacherSchoolViewSet, basename='teachers-school')
router.register(r'parents', ParentOfStudentViewSet, basename='parents')
router.register(r'users', UserViewSet, basename='users')
router.register(r'get-current-user', CurrentUserViewSet, basename='get-current-user')

# URL FOR SCHOOL MANAGER
router.register(r'school-years', SchoolYearViewSet, basename='schoolyear')
router.register(r'active-schoolyear', ActiveSchoolYearViewSet, basename='active-schoolyear')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'inscriptions', InscriptionViewSet, basename="inscriptions")
router.register(r'student-evaluations', StudentEvaluationViewSet, basename="student-evaluations")

#URL FOR SUBJECT MANAGER
router.register(r'school-calendars', SchoolCalendarViewSet, basename='schoolcalendar')
router.register(r'school-holidays', SchoolHolidayViewSet, basename='schoolholiday')
router.register(r'school-programs', SchoolProgramViewSet, basename='schoolprogram')
router.register(r'school-schedules', SchoolScheduleViewSet, basename='schoolschedule')
router.register(r'subject-attributions', SubjectAttributionViewSet, basename='subject-attribution')

# URL FOR ADMIN MANAGER
router.register(r'school-cycles', SchoolCycleViewSet, basename='schoolcycle')
router.register(r'school-series', SchoolSeriesViewSet, basename='schoolseries')
router.register(r'school-levels', SchoolLevelViewSet, basename='schoollevel')
router.register(r'subject-groups', SubjectGroupViewSet, basename='subjectgroup')
router.register(r'document-types', DocumentTypeViewSet, basename='documenttype')
router.register(r'sanction-appreciation-types', SanctionOrAppreciationTypeViewSet, basename='sanctionappreciationtype')

# URL FORM COMMUNICATION MANAGER
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'informations', InformationViewSet, basename='informations')
router.register(r'evenements', EventViewSet, basename='events')
router.register(r'annonces', AnnouncementViewSet, basename='announcements')

# URL FOR LIBRARY MANAGER
router.register(r'ebooks', EbookViewSet, basename='ebooks')


urlpatterns = [
    path('', include(router.urls)),
    path('school-statistics/', SchoolStatisticsView.as_view(), name='school-statistics'),
    path('active-school-year-students/', ActiveSchoolYearStudentsView.as_view(), name='active-school-year-students'),
    #URL FOR AUTHENTICATION
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
