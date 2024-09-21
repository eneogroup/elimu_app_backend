from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.auth.authentication_api import LoginAPIView, LogoutAPIView
from .views.admin_manager.admin_manager_views import (
    SchoolCycleList, SchoolCycleDetail,
    SchoolSeriesList, SchoolSeriesDetail,
    SchoolLevelList, SchoolLevelDetail,
    SubjectGroupList, SubjectGroupDetail,
    DocumentTypeList, DocumentTypeDetail,
    SanctionOrAppreciationTypeList, SanctionOrAppreciationTypeDetail,
)
from .views.school_manager.school_manager_view import (
    SchoolYearListCreateAPIView, SchoolYearRetrieveUpdateDestroyAPIView,
    ClassroomListCreateAPIView, ClassroomRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    
    #URL FOR AUTHENTICATION
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    #URL FOR ADMIN MANAGER
    path('school-cycles/', SchoolCycleList.as_view(), name='school_cycle_list'),
    path('school-cycles/<int:pk>/', SchoolCycleDetail.as_view(), name='school_cycle_detail'),
    path('school-series/', SchoolSeriesList.as_view(), name='school_series_list'),
    path('school-series/<int:pk>/', SchoolSeriesDetail.as_view(), name='school_series_detail'),
    path('school-levels/', SchoolLevelList.as_view(), name='school_level_list'),
    path('school-levels/<int:pk>/', SchoolLevelDetail.as_view(), name='school_level_detail'),
    path('subject-groups/', SubjectGroupList.as_view(), name='subject_group_list'),
    path('subject-groups/<int:pk>/', SubjectGroupDetail.as_view(), name='subject_group_detail'),
    path('document-types/', DocumentTypeList.as_view(), name='document_type_list'),
    path('document-types/<int:pk>/', DocumentTypeDetail.as_view(), name='document_type_detail'),
    path('sanction-appreciation-types/', SanctionOrAppreciationTypeList.as_view(), name='sanction_appreciation_type_list'),
    path('sanction-appreciation-types/<int:pk>/', SanctionOrAppreciationTypeDetail.as_view(), name='sanction_appreciation_type_detail'),
    
    #URL FOR SCHOOL MANAGER
    path('school-years/', SchoolYearListCreateAPIView.as_view(), name='school_year_list'),
    path('school-years/<int:pk>/', SchoolYearRetrieveUpdateDestroyAPIView.as_view(), name='school_year_detail'),
    path('classrooms/', ClassroomListCreateAPIView.as_view(), name='classroom_list'),
    path('classrooms/<int:pk>/', ClassroomRetrieveUpdateDestroyAPIView.as_view(), name='classroom_detail'),
]
