from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from backend.models.account import ParentOfStudent, TeacherSchool
from backend.models.school_manager import Inscription, SchoolAbsence, SchoolYear, Classroom, StudentEvaluation
from api.serializers.school_manager_serializer import InscriptionSerializer, SchoolAbsenceSerializer, SchoolYearSerializer, ClassroomSerializer, StudentEvaluationSerializer
from backend.permissions.permission_app import IsDirector, IsManager
from rest_framework.decorators import action



class SchoolStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet qui renvoie les statistiques de l'école pour les enseignants, élèves inscrits et parents des élèves inscrits.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='statistics')
    def get_statistics(self, request):
        user = request.user
        
        # Filtrer par l'école de l'utilisateur connecté
        school_code = user.school_code
        
        # Nombre total des enseignants dans l'école de l'utilisateur connecté
        total_teachers = TeacherSchool.objects.filter(school_code=school_code).count()
        
        # Nombre total des élèves inscrits dans l'année scolaire active
        total_pupils = Inscription.objects.filter(
            classroom__school=school_code,
            is_active=True,
            school_year__is_current_year=True
        ).count()
        
        # Extraire tous les élèves inscrits
        inscriptions = Inscription.objects.filter(
            classroom__school=school_code, 
            is_active=True, 
            school_year__is_current_year=True
        )
        pupils = [inscription.student for inscription in inscriptions]

        # Récupérer tous les parents des élèves inscrits
        parents = ParentOfStudent.objects.filter(parents_of_pupils__in=pupils).distinct()

        # Retourner les données dans la réponse
        return Response({
            "total_teachers": total_teachers,
            "total_pupils": total_pupils,
            "total_parents": parents.count(),
        })


class SchoolYearViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolYearSerializer

    def get_queryset(self):
        # Filtrer les années scolaires de l'école de l'utilisateur connecté
        return SchoolYear.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        # Associer l'année scolaire à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school!=request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette année scolaire."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school!=request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette année scolaire."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class ActiveSchoolYearViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SchoolYearSerializer
    permission_classes = [permissions.IsAuthenticated]  # Les utilisateurs doivent être authentifiés

    def get_queryset(self):
        """
        Récupérer l'année scolaire active pour l'école de l'utilisateur connecté.
        """
        user = self.request.user
        return SchoolYear.objects.filter(is_current_year=True, school=user.school_code)

    def list(self, request, *args, **kwargs):
        """
        Retourner les informations de l'année scolaire active de l'école de l'utilisateur connecté.
        Si aucune n'est active, retourner une réponse vide.
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Aucune année scolaire active trouvée pour cette école."}, status=404)
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)


class ClassroomViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        # Filtrer les salles de classe par l'école de l'utilisateur connecté
        return Classroom.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        # Associer la salle de classe à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school!=request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette salle de classe."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school!=request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette salle de classe."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class InscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InscriptionSerializer

    def get_queryset(self):
        return Inscription.objects.filter(classroom__school=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classroom.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette inscription."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classroom.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette inscription."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classroom.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher cette inscription."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class StudentEvaluationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentEvaluationSerializer

    def get_queryset(self):
        return StudentEvaluation.objects.filter(inscription__classroom__school=self.request.user.school_code)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.inscription.classroom.school != request.user.teacherschool.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette évaluation."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.inscription.classroom.school != request.user.teacherschool.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette évaluation."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)



class ActiveSchoolYearStudentsViewSet(viewsets.ViewSet):
    """
    ViewSet pour récupérer les élèves inscrits pendant l'année scolaire active de l'école de l'utilisateur connecté.
    """
    permission_classes = [permissions.IsAuthenticated]  # Exige que l'utilisateur soit authentifié

    @action(detail=False, methods=['get'], url_path='active-school-year-students')
    def get_active_school_year_students(self, request):
        # Récupérer le code de l'école de l'utilisateur connecté
        school_code = request.user.school_code

        # Récupérer l'année scolaire active de l'école
        try:
            active_school_year = SchoolYear.objects.get(is_current_year=True, school=school_code)
        except SchoolYear.DoesNotExist:
            return Response({"detail": "Aucune année scolaire active trouvée."}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer les inscriptions des élèves pour l'année scolaire active
        inscriptions = Inscription.objects.filter(school_year=active_school_year, classroom__school=school_code)

        # Sérialiser les données des inscriptions
        serializer = InscriptionSerializer(inscriptions, many=True)

        # Renvoyer les informations des élèves inscrits
        return Response(serializer.data, status=status.HTTP_200_OK)



class SchoolAbsenceViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolAbsenceSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager, IsDirector]
    
    def get_queryset(self):
        return SchoolAbsence.objects.filter(classroom__school=self.request.user.school_code)


    def create(self, request, *args, **kwargs):
        """Personnalise la création pour gérer des validations supplémentaires ou des logiques complexes"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """Personnalise la mise à jour d'une absence"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Personnalise la suppression d'une absence"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
