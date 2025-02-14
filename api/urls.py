from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.account_view import CurrentUserViewSet, ParentsViewSet, PasswordResetConfirmView, PasswordResetView, PupilsViewSet, TeachersViewSet, UserViewSet
from api.views.auth.authentication_api import LoginViewSet, LogoutAPIView
from rest_framework.routers import DefaultRouter
from api.views.communication_view import AnnouncementViewSet, EventViewSet, InformationViewSet, MessageViewSet, TagViewSet
from api.views.facturation_view import ExpenseCategoryViewSet, SchoolExpenseViewSet, SchoolInvoiceViewSet, SchoolPaymentTrackingViewSet
from api.views.library_view import EbookViewSet, MaterialRequestViewSet, SchoolMaterialViewSet
from api.views.subject_manager_view import SchoolCalendarViewSet, SchoolHolidayViewSet, SchoolProgramViewSet, SchoolReportCardViewSet, SchoolScheduleViewSet, SubjectAttributionViewSet, SubjectViewSet
from .views.admin_manager_views import *
from .views.school_manager_view import (
    ActiveSchoolYearStudentsViewSet, ActiveSchoolYearViewSet, InscriptionViewSet, SchoolAbsenceViewSet, SchoolGeneralConfigViewSet, SchoolStatisticsViewSet, SchoolYearViewSet, ClassroomViewSet, StudentEvaluationViewSet
)

router = DefaultRouter()

# URL FOR ADMIN & MANAGER
router.register(r'school-general-config', SchoolGeneralConfigViewSet, basename='school-general-config')
router.register(r'academic-year-of-school', SchoolYearViewSet, basename='academic-year-of-school')
router.register(r'current-school-year', ActiveSchoolYearViewSet, basename='current-school-year')
router.register(r'parent-of-students', ParentsViewSet, basename='parent-of-students')
router.register(r'students-of-school', PupilsViewSet, basename='students-of-school')
router.register(r'teachers-of-school', TeachersViewSet, basename='teachers-of-school')
router.register(r'subjet-of-school', SubjectViewSet, basename='subjet-of-school')
router.register(r'subject-attribution', SubjectAttributionViewSet, basename='subject-attribution')
# router.register(r'school-calendar', SchoolCalendarViewSet, basename='school-calendar')
# router.register(r'school-holiday', SchoolHolidayViewSet, basename='school-holiday')
# router.register(r'school-program', SchoolProgramViewSet, basename='school-program')
router.register(r'schedules-of-school', SchoolScheduleViewSet, basename='schedules-of-school')
# router.register(r'school-report-card', SchoolReportCardViewSet, basename='school-report-card')
router.register(r'classrooms-of-school', ClassroomViewSet, basename='classrooms-of-school')
router.register(r'inscription-of-students', InscriptionViewSet, basename='inscription-of-students')
router.register(r'active-students-of-school', ActiveSchoolYearStudentsViewSet, basename='active-students-of-school')
# router.register(r'school-absence', SchoolAbsenceViewSet, basename='school-absence')
router.register(r'students-evaluation', StudentEvaluationViewSet, basename='students-evaluation')
router.register(r'school-statistics', SchoolStatisticsViewSet, basename='school-statistics')
# router.register(r'expense-category', ExpenseCategoryViewSet, basename='expense-category')
# router.register(r'school-expense', SchoolExpenseViewSet, basename='school-expense')
router.register(r'school-invoices', SchoolInvoiceViewSet, basename='school-invoices')
# router.register(r'school-payment-tracking', SchoolPaymentTrackingViewSet, basename='school-payment-tracking')
# router.register(r'ebook-of-school', EbookViewSet, basename='ebook-of-school')
# router.register(r'material-request', MaterialRequestViewSet, basename='material-request')
# router.register(r'school-material', SchoolMaterialViewSet, basename='school-material')
# router.register(r'announcement', AnnouncementViewSet, basename='announcement')
# router.register(r'event', EventViewSet, basename='event')
# router.register(r'information', InformationViewSet, basename='information')
# router.register(r'message', MessageViewSet, basename='message')
# router.register(r'tag', TagViewSet, basename='tag')
# URL FOR USER
router.register(r'user/account/view/current-user', CurrentUserViewSet, basename='current-user')
# router.register(r'user/account/view/user', UserViewSet, basename='user')
# URL FOR AUTH
router.register(r'auth', LoginViewSet, basename='auth')

urlpatterns = [
    path('admin&manager/account/view/', include(router.urls)),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth_logout'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/account/view/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('user/account/view/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
