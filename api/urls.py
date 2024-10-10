from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.account_view import CurrentUserViewSet, ParentOfStudentViewSet, ParentsOfStudentsInSchoolViewSet, PasswordResetConfirmView, PasswordResetView, PupilsViewset, TeacherSchoolViewSet, UserViewSet
from api.views.auth.authentication_api import LoginViewSet, LogoutAPIView
from rest_framework.routers import DefaultRouter
from api.views.communication_view import AnnouncementViewSet, EventViewSet, InformationViewSet, MessageViewSet, TagViewSet
from api.views.facturation_view import ExpenseCategoryViewSet, SchoolExpenseViewSet, SchoolInvoiceViewSet, SchoolPaymentTrackingViewSet
from api.views.library_view import EbookViewSet, MaterialRequestViewSet, SchoolMaterialViewSet
from api.views.subject_manager_view import SchoolCalendarViewSet, SchoolHolidayViewSet, SchoolProgramViewSet, SchoolReportCardViewSet, SchoolScheduleViewSet, SubjectAttributionViewSet, SubjectViewSet
from .views.admin_manager_views import *
from .views.school_manager_view import (
    ActiveSchoolYearStudentsViewSet, ActiveSchoolYearViewSet, InscriptionViewSet, SchoolAbsenceViewSet, SchoolStatisticsViewSet, SchoolYearViewSet, ClassroomViewSet, StudentEvaluationViewSet
)

router = DefaultRouter()

# URL FOR ACCOUNT
router.register(r'teachers-school', TeacherSchoolViewSet, basename='teachers-school')
router.register(r'parents', ParentOfStudentViewSet, basename='parents')
router.register(r'parents-of-student-school', ParentsOfStudentsInSchoolViewSet, basename='parents-of-student-school')
router.register(r'users', UserViewSet, basename='users')
router.register(r'get-current-user', CurrentUserViewSet, basename='get-current-user')

# URL FOR SCHOOL MANAGER
router.register(r'school-years', SchoolYearViewSet, basename='schoolyear')
router.register(r'active-schoolyear', ActiveSchoolYearViewSet, basename='active-schoolyear')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'inscriptions', InscriptionViewSet, basename="inscriptions")
router.register(r'student-evaluations', StudentEvaluationViewSet, basename="student-evaluations")
# router.register(r'school-absences', SchoolAbsenceViewSet, basename='school-absence')
router.register(r'school-statistics', SchoolStatisticsViewSet, basename='school-statistics')
router.register(r'students', ActiveSchoolYearStudentsViewSet, basename='students')
router.register(r'pupils', PupilsViewset, basename='pupils')


#URL FOR SUBJECT MANAGER
router.register(r'school-subject', SubjectViewSet, basename='school-subject')
# router.register(r'school-calendars', SchoolCalendarViewSet, basename='schoolcalendar')
# router.register(r'school-holidays', SchoolHolidayViewSet, basename='schoolholiday')
# router.register(r'school-programs', SchoolProgramViewSet, basename='schoolprogram')
router.register(r'school-schedules', SchoolScheduleViewSet, basename='schoolschedule')
router.register(r'subject-attributions', SubjectAttributionViewSet, basename='subject-attribution')
router.register(r'school-report-cards', SchoolReportCardViewSet, basename='school-report-card')


# URL FOR ADMIN MANAGER
router.register(r'school-cycles', SchoolCycleViewSet, basename='schoolcycle')
router.register(r'school-series', SchoolSeriesViewSet, basename='schoolseries')
router.register(r'school-levels', SchoolLevelViewSet, basename='schoollevel')
router.register(r'subject-groups', SubjectGroupViewSet, basename='subjectgroup')
# router.register(r'document-types', DocumentTypeViewSet, basename='documenttype')
# router.register(r'sanction-appreciation-types', SanctionOrAppreciationTypeViewSet, basename='sanctionappreciationtype')

# URL FORM COMMUNICATION MANAGER
# router.register(r'tags', TagViewSet, basename='tags')
# router.register(r'informations', InformationViewSet, basename='informations')
# router.register(r'evenements', EventViewSet, basename='events')
router.register(r'annonces', AnnouncementViewSet, basename='announcements')
# router.register(r'messages', MessageViewSet, basename='messages')

# URL FOR LIBRARY MANAGER
router.register(r'ebooks', EbookViewSet, basename='ebooks')
# router.register(r'materials', SchoolMaterialViewSet, basename='materials')
# router.register(r'material-requests', MaterialRequestViewSet, basename='school-material-requests')

# URL FOR FACTURATION
router.register(r'school-invoices', SchoolInvoiceViewSet, basename='school-invoice')
# router.register(r'school-payment-tracking', SchoolPaymentTrackingViewSet, basename='school-payment-tracking')
# router.register(r'school-expense-categories', ExpenseCategoryViewSet, basename='school-expense-categories')
# router.register(r'school-expenses', SchoolExpenseViewSet, basename="school-expenses")

#URL FOR AUTHENTICATION
router.register(r'auth', LoginViewSet, basename='auth')


urlpatterns = [
    path('', include(router.urls)),
    #URL FOR AUTHENTICATION
    # path('logout/', LogoutAPIView.as_view(), name='logout'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    # path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
