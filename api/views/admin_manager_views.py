from rest_framework import viewsets, permissions
from backend.models.admin_manager import SchoolCycle, SchoolSeries, SchoolLevel, SubjectGroup, DocumentType, SanctionOrAppreciationType
from api.serializers.admin_manager_serializer import (
    SchoolCycleSerializer, SchoolSeriesSerializer,
    SchoolLevelSerializer, SubjectGroupSerializer,
    DocumentTypeSerializer, SanctionOrAppreciationTypeSerializer
)


class SchoolCycleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing SchoolCycle instances.

    Attributes:
        permission_classes (list): A list of permission classes that the user must satisfy to access this viewset.
        queryset (QuerySet): The queryset that represents all SchoolCycle instances.
        serializer_class (Serializer): The serializer class used to validate and serialize SchoolCycle instances.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SchoolCycle.objects.all()
    serializer_class = SchoolCycleSerializer


class SchoolSeriesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing SchoolSeries instances.

    Attributes:
        permission_classes (list): A list of permission classes that the user must satisfy to access this viewset.
        queryset (QuerySet): A queryset containing all SchoolSeries instances.
        serializer_class (Serializer): The serializer class used to validate and serialize SchoolSeries instances.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SchoolSeries.objects.all()
    serializer_class = SchoolSeriesSerializer


class SchoolLevelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing school level instances.

    Attributes:
        permission_classes (list): A list of permission classes that the user must pass to access this viewset.
        queryset (QuerySet): The queryset that represents all the school level instances.
        serializer_class (Serializer): The serializer class used to validate and serialize the school level instances.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SchoolLevel.objects.all()
    serializer_class = SchoolLevelSerializer


class SubjectGroupViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing SubjectGroup instances.

    Attributes:
        permission_classes (list): A list of permission classes that the user must pass to access the view.
        queryset (QuerySet): The queryset that should be used for returning objects from this view.
        serializer_class (Serializer): The serializer class that should be used for validating and deserializing input, and for serializing output.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubjectGroup.objects.all()
    serializer_class = SubjectGroupSerializer


class DocumentTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing document types.

    Attributes:
        permission_classes (list): A list of permission classes that the user must satisfy to access this viewset.
        queryset (QuerySet): The queryset that represents all DocumentType objects.
        serializer_class (Serializer): The serializer class used to validate and serialize the DocumentType objects.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class SanctionOrAppreciationTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing SanctionOrAppreciationType instances.

    This viewset provides `list`, `create`, `retrieve`, `update`, and `destroy` actions for the SanctionOrAppreciationType model.

    Attributes:
        permission_classes (list): A list of permission classes that the user must pass to access this viewset.
        queryset (QuerySet): The queryset that represents all instances of the SanctionOrAppreciationType model.
        serializer_class (Serializer): The serializer class used to validate and deserialize input, and serialize output.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SanctionOrAppreciationType.objects.all()
    serializer_class = SanctionOrAppreciationTypeSerializer
