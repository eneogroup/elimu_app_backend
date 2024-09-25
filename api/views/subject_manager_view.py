from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from api.serializers.subject_manager_serializer import SchoolCalendarSerializer, SchoolHolidaySerializer, SchoolProgramSerializer, SchoolScheduleSerializer, SubjectSerializer
from backend.models.subject_manager import SchoolCalendar, SchoolHoliday, SchoolProgram, SchoolSchedule, Subject


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette matière."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette matière."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher cette matière."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)



class SchoolScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolScheduleSerializer

    def get_queryset(self):
        return SchoolSchedule.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cet emploi du temps."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cet emploi du temps."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher cet emploi du temps."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    

class SchoolCalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolCalendarSerializer

    def get_queryset(self):
        return SchoolCalendar.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier ce calendrier."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer ce calendrier."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher ce calendrier."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)


class SchoolHolidayViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolHolidaySerializer

    def get_queryset(self):
        return SchoolHoliday.objects.filter(school=self.request.user.teacherschool.school_code)

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier ce congé."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer ce congé."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher ce congé."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)



class SchoolProgramViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolProgramSerializer

    def get_queryset(self):
        return SchoolProgram.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier ce programme."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer ce programme."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher ce programme."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)
    
