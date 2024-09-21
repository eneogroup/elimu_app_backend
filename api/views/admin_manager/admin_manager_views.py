from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from backend.models.admin_manager.admin_manager import SchoolCycle, SchoolSeries, SchoolLevel, SubjectGroup, DocumentType, SanctionOrAppreciationType
from api.serializers.admin_manager.admin_manager_serializer import (
    SchoolCycleSerializer,
    SchoolSeriesSerializer,
    SchoolLevelSerializer,
    SubjectGroupSerializer,
    DocumentTypeSerializer,
    SanctionOrAppreciationTypeSerializer
)

class SchoolCycleList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SchoolCycle.objects.all()
    serializer_class = SchoolCycleSerializer

class SchoolCycleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SchoolCycle.objects.all()
    serializer_class = SchoolCycleSerializer

class SchoolSeriesList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SchoolSeries.objects.all()
    serializer_class = SchoolSeriesSerializer

class SchoolSeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SchoolSeries.objects.all()
    serializer_class = SchoolSeriesSerializer

class SchoolLevelList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SchoolLevel.objects.all()
    serializer_class = SchoolLevelSerializer

class SchoolLevelDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SchoolLevel.objects.all()
    serializer_class = SchoolLevelSerializer

class SubjectGroupList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer

class SubjectGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer

class DocumentTypeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class DocumentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

class SanctionOrAppreciationTypeList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SanctionOrAppreciationType.objects.all()
    serializer_class = SanctionOrAppreciationTypeSerializer

class SanctionOrAppreciationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SanctionOrAppreciationType.objects.all()
    serializer_class = SanctionOrAppreciationTypeSerializer
