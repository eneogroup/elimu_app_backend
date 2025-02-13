from django.forms import ValidationError
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from api.serializers.subject_manager_serializer import SchoolCalendarSerializer, SchoolHolidaySerializer, SchoolProgramSerializer, SchoolReportCardSerializer, SchoolScheduleSerializer, SubjectAttributionSerializer, SubjectSerializer
from backend.constant import get_user_school
from backend.models.subject_manager import SchoolCalendar, SchoolHoliday, SchoolProgram, SchoolReportCard, SchoolSchedule, Subject, SubjectAttribution
from backend.permissions.permission_app import IsDirector, IsManager
from rest_framework.decorators import action



class SubjectViewSet(viewsets.ModelViewSet):
    """
    SubjectViewSet is a viewset for managing Subject objects.
    Attributes:
        permission_classes (list): The list of permission classes that are required to access this viewset.
        serializer_class (SubjectSerializer): The serializer class used for Subject objects.
    Methods:
        get_queryset(self):
            Returns the queryset of Subject objects filtered by the school of the current user.
        perform_create(self, serializer):
            Validates and saves the Subject object. Handles validation errors.
        update(self, request, *args, **kwargs):
            Updates an existing Subject object. Validates the data and returns a response with the updated object.
            Checks if the user has permission to update the subject.
        destroy(self, request, *args, **kwargs):
            Deletes an existing Subject object. Returns a response with no content.
            Checks if the user has permission to delete the subject.
        retrieve(self, request, *args, **kwargs):
            Retrieves a specific Subject object. Returns a response with the serialized object.
            Checks if the user has permission to retrieve the subject.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(school=get_user_school(self.request))

    def perform_create(self, serializer):
        serializer.save(school=get_user_school(self.request))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier cette matière."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer cette matière."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas afficher cette matière."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)


class SchoolScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school schedules.

    This ViewSet provides the following actions:
    - list: Retrieve a list of school schedules.
    - create: Create a new school schedule.
    - retrieve: Retrieve a specific school schedule.
    - update: Update an existing school schedule.
    - partial_update: Partially update an existing school schedule.
    - destroy: Delete a school schedule.

    Permissions:
    - Only authenticated users can access these endpoints.

    Methods:
    - get_queryset: Returns the queryset of school schedules for the user's school.
    - perform_create: Saves a new school schedule for the user's school.
    - update: Updates a school schedule if it belongs to the user's school.
    - destroy: Deletes a school schedule if it belongs to the user's school.
    - retrieve: Retrieves a school schedule if it belongs to the user's school.

    Responses:
    - Returns a 403 Forbidden response if the user attempts to access or modify a schedule that does not belong to their school.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolScheduleSerializer

    def get_queryset(self):
        return SchoolSchedule.objects.filter(school=get_user_school(self.request))

    def perform_create(self, serializer):
        serializer.save(school=get_user_school(self.request))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier cet emploi du temps."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer cet emploi du temps."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas afficher cet emploi du temps."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    

class SchoolCalendarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school calendars.
    This ViewSet provides the following actions:
    - list: Retrieve a list of school calendars.
    - create: Create a new school calendar.
    - retrieve: Retrieve a specific school calendar.
    - update: Update a specific school calendar.
    - partial_update: Partially update a specific school calendar.
    - destroy: Delete a specific school calendar.
    Permissions:
    - Only authenticated users can access these endpoints.
    Methods:
    - get_queryset: Returns the queryset of school calendars filtered by the user's school.
    - perform_create: Saves a new school calendar with the user's school.
    - update: Updates a school calendar if it belongs to the user's school.
    - destroy: Deletes a school calendar if it belongs to the user's school.
    - retrieve: Retrieves a school calendar if it belongs to the user's school.
    Responses:
    - Returns a 403 Forbidden response if the user attempts to access or modify a calendar that does not belong to their school.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolCalendarSerializer

    def get_queryset(self):
        return SchoolCalendar.objects.filter(school=get_user_school(self.request))

    def perform_create(self, serializer):
        serializer.save(school=get_user_school(self.request))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier ce calendrier."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer ce calendrier."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas afficher ce calendrier."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)


class SchoolHolidayViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school holidays.
    This ViewSet provides the following actions:
    - list: Retrieve a list of school holidays.
    - create: Create a new school holiday.
    - retrieve: Retrieve a specific school holiday.
    - update: Update a specific school holiday.
    - partial_update: Partially update a specific school holiday.
    - destroy: Delete a specific school holiday.
    Permissions:
    - Only authenticated users can access these endpoints.
    Methods:
    - get_queryset: Returns the queryset of school holidays filtered by the user's school.
    - perform_create: Saves a new school holiday with the user's school.
    - update: Updates a school holiday if it belongs to the user's school.
    - destroy: Deletes a school holiday if it belongs to the user's school.
    - retrieve: Retrieves a school holiday if it belongs to the user's school.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolHolidaySerializer

    def get_queryset(self):
        return SchoolHoliday.objects.filter(school=get_user_school(self.request))

    def perform_create(self, serializer):
        serializer.save(school=get_user_school(self.request))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier ce congé."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer ce congé."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas afficher ce congé."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)



class SchoolProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing SchoolProgram instances.
    This ViewSet provides the following actions:
    - list: Retrieve a list of SchoolProgram instances.
    - create: Create a new SchoolProgram instance.
    - retrieve: Retrieve a specific SchoolProgram instance.
    - update: Update a specific SchoolProgram instance.
    - partial_update: Partially update a specific SchoolProgram instance.
    - destroy: Delete a specific SchoolProgram instance.
    Permissions:
    - Only authenticated users can access these actions.
    Methods:
    - get_queryset: Returns the queryset of SchoolProgram instances filtered by the user's school.
    - perform_create: Saves a new SchoolProgram instance with the user's school.
    - update: Updates a SchoolProgram instance if it belongs to the user's school.
    - destroy: Deletes a SchoolProgram instance if it belongs to the user's school.
    - retrieve: Retrieves a SchoolProgram instance if it belongs to the user's school.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolProgramSerializer

    def get_queryset(self):
        return SchoolProgram.objects.filter(school=get_user_school(self.request))

    def perform_create(self, serializer):
        serializer.save(school=get_user_school(self.request))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier ce programme."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer ce programme."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas afficher ce programme."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    


class SubjectAttributionViewSet(viewsets.ModelViewSet):
    """
    SubjectAttributionViewSet is a viewset for managing SubjectAttribution objects.
    Attributes:
        serializer_class (SubjectAttributionSerializer): The serializer class used for SubjectAttribution objects.
        permission_classes (list): The list of permission classes that are required to access this viewset.
    Methods:
        get_queryset(self):
            Returns the queryset of SubjectAttribution objects filtered by the school of the current user.
        create(self, request, *args, **kwargs):
            Creates a new SubjectAttribution object. Validates the data and returns a response with the created object.
        perform_create(self, serializer):
            Validates and saves the SubjectAttribution object. Handles validation errors.
        update(self, request, *args, **kwargs):
            Updates an existing SubjectAttribution object. Validates the data and returns a response with the updated object.
        perform_update(self, serializer):
            Validates and updates the SubjectAttribution object. Handles validation errors.
        destroy(self, request, *args, **kwargs):
            Deletes an existing SubjectAttribution object. Returns a response with no content.
        perform_destroy(self, instance):
            Deletes the SubjectAttribution object.
    """
    serializer_class = SubjectAttributionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SubjectAttribution.objects.filter(subject__school=get_user_school(self.request))
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Valider et sauvegarder l'objet SubjectAttribution
        try:
            serializer.save()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        # Valider et mettre à jour l'objet
        try:
            serializer.save()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class SchoolReportCardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school report cards.
    Endpoints:
    - `GET /schoolreportcard/by-student/<student_id>/`: Get report cards by student.
    - `GET /schoolreportcard/by-subject/<subject_id>/`: Get report cards by subject.
    - `GET /schoolreportcard/average-by-student-subject/<student_id>/<subject_id>/`: Get average grade for a student in a subject.
    - `GET /schoolreportcard/passing-status/<student_id>/<subject_id>/`: Get passing status for a student in a subject.
    - `GET /schoolreportcard/summary/<student_id>/`: Get summary of report cards for a student.
    - `GET /schoolreportcard/by-school/<school_id>/`: Get report cards by school.
    Methods:
    - `get_queryset()`: Returns the queryset of report cards filtered by the user's school.
    - `perform_create(serializer)`: Saves a new report card with the user's school.
    - `perform_update(serializer)`: Updates an existing report card with the user's school.
    - `perform_destroy(instance)`: Deletes a report card.
    - `get_by_student(request, student_id)`: Returns report cards for a specific student.
    - `get_by_subject(request, subject_id)`: Returns report cards for a specific subject.
    - `get_average_by_student_subject(request, student_id, subject_id)`: Returns the average grade for a student in a specific subject.
    - `get_passing_status(request, student_id, subject_id)`: Returns the passing status for a student in a specific subject.
    - `get_summary(request, student_id)`: Returns a summary of report cards for a specific student.
    - `get_by_school(request, school_id)`: Returns report cards for a specific school.
    """
    serializer_class = SchoolReportCardSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        return SchoolReportCard.objects.filter(school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        serializer.save(school=get_user_school(self.request))
    
    def perform_update(self, serializer):
        return serializer.save(school=get_user_school(self.request))
    
    def perform_destroy(self, instance):
        instance.delete()
    
    # Endpoint pour obtenir les rapports par élève
    @action(detail=False, methods=['get'], url_path='by-student/(?P<student_id>[^/.]+)')
    def get_by_student(self, request, student_id=None):
        report_cards = SchoolReportCard.objects.filter(student__id=student_id, school=get_user_school(request))
        serializer = self.get_serializer(report_cards, many=True)
        return Response(serializer.data)

    # Endpoint pour obtenir les rapports par matière
    @action(detail=False, methods=['get'], url_path='by-subject/(?P<subject_id>[^/.]+)')
    def get_by_subject(self, request, subject_id=None):
        report_cards = SchoolReportCard.objects.filter(subject__id=subject_id, school=get_user_school(request))
        serializer = self.get_serializer(report_cards, many=True)
        return Response(serializer.data)

    # Endpoint pour calculer la moyenne pour un élève dans une matière
    @action(detail=False, methods=['get'], url_path='average-by-student-subject/(?P<student_id>[^/.]+)/(?P<subject_id>[^/.]+)')
    def get_average_by_student_subject(self, request, student_id=None, subject_id=None):
        report_cards = SchoolReportCard.objects.filter(student__id=student_id, subject__id=subject_id, school=get_user_school(request))
        if report_cards.exists():
            average = sum(int(report_card.grade) for report_card in report_cards) / len(report_cards)
            return Response({"average_grade": average})
        return Response({"error": "No report cards found for the given student and subject."}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint pour obtenir le statut de réussite/échec d'un élève dans une matière
    @action(detail=False, methods=['get'], url_path='passing-status/(?P<student_id>[^/.]+)/(?P<subject_id>[^/.]+)')
    def get_passing_status(self, request, student_id=None, subject_id=None):
        report_cards = SchoolReportCard.objects.filter(student__id=student_id, subject__id=subject_id, school=get_user_school(request))
        if report_cards.exists():
            average_grade = sum(int(report_card.grade) for report_card in report_cards) / len(report_cards)
            if average_grade >= 10:
                return Response({"status": "Passing"})
            else:
                return Response({"status": "Failing"})
        return Response({"error": "No report cards found for the given student and subject."}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint pour obtenir un résumé du bulletin d'un élève
    @action(detail=False, methods=['get'], url_path='summary/(?P<student_id>[^/.]+)')
    def get_summary(self, request, student_id=None):
        report_cards = SchoolReportCard.objects.filter(student__id=student_id, school=get_user_school(request))
        if report_cards.exists():
            summary = {
                "total_subjects": report_cards.count(),
                "average_grade": sum(int(report_card.grade) for report_card in report_cards) / len(report_cards),
                "grades": [
                    {
                        "subject": report_card.subject.name,
                        "grade": report_card.grade,
                        "is_passing": int(report_card.grade) >= 10
                    }
                    for report_card in report_cards
                ]
            }
            return Response(summary)
        return Response({"error": "No report cards found for the given student."}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint pour filtrer les bulletins par école
    @action(detail=False, methods=['get'], url_path='by-school/(?P<school_id>[^/.]+)')
    def get_by_school(self, request, school_id=None):
        report_cards = SchoolReportCard.objects.filter(school__id=school_id)
        serializer = self.get_serializer(report_cards, many=True)
        return Response(serializer.data)

