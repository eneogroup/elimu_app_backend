from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers.facturation_serializer import PaymentTrackingSerializer
from backend.models.facturation import PaymentTracking

class SchoolPaymentTrackingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue API qui permet de récupérer le suivi des paiements des frais de scolarité.
    """
    serializer_class = PaymentTrackingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtrer les suivis de paiements pour les frais de scolarité d'un utilisateur spécifique (élève ou parent).
        """
        user = self.request.user
        if user.is_admin:
            return PaymentTracking.objects.all()  # Les administrateurs peuvent voir tous les suivis
        elif user.role.name == 'Gestionnaire' or user.role.name == 'Directeur':
            # Pour les parents ou élèves, filtrer les paiements liés à leurs factures
            return PaymentTracking.objects.filter(payment__invoice__school=user.school_code)
