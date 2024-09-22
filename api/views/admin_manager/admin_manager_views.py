from rest_framework import viewsets, permissions
from backend.models.admin_manager.admin_manager import SchoolCycle, SchoolSeries, SchoolLevel, SubjectGroup, DocumentType, SanctionOrAppreciationType
from api.serializers.admin_manager.admin_manager_serializer import (
    SchoolCycleSerializer, SchoolSeriesSerializer,
    SchoolLevelSerializer, SubjectGroupSerializer,
    DocumentTypeSerializer, SanctionOrAppreciationTypeSerializer
)


class SchoolCycleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SchoolCycle.objects.all()
    serializer_class = SchoolCycleSerializer


class SchoolSeriesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SchoolSeries.objects.all()
    serializer_class = SchoolSeriesSerializer


class SchoolLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SchoolLevel.objects.all()
    serializer_class = SchoolLevelSerializer


class SubjectGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer


class DocumentTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class SanctionOrAppreciationTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SanctionOrAppreciationType.objects.all()
    serializer_class = SanctionOrAppreciationTypeSerializer
