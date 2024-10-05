import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from api.serializers.facturation_serializer import ExpenseCategorySerializer, PaymentTrackingSerializer, SchoolExpenseSerializer, SchoolInvoiceSerializer
from backend.models.facturation import ExpenseCategory, PaymentTracking, SchoolExpense, SchoolInvoice
from backend.permissions.permission_app import IsDirector, IsManager



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





class SchoolInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SchoolInvoice.objects.all()
    serializer_class = SchoolInvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Récupère toutes les factures de l'école de l'utilisateur connecté (ou un filtre personnalisé)."""
        return SchoolInvoice.objects.filter(school=self.request.user.school_code)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """Marquer une facture comme payée."""
        invoice = self.get_object()
        amount = request.data.get('amount')
        
        if amount:
            invoice.mark_as_paid(amount=amount)
            return Response({'status': 'Facture marquée comme payée'}, status=status.HTTP_200_OK)
        return Response({'error': 'Le montant est requis'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def send_invoice_email(self, request, pk=None):
        """Envoyer la facture par email à l'élève."""
        invoice = self.get_object()
        try:
            invoice.send_invoice_email()
            return Response({'status': 'Facture envoyée par email'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def payment_history(self, request, pk=None):
        """Obtenir l'historique des paiements pour une facture."""
        invoice = self.get_object()
        payment_history = invoice.get_payment_history()
        return Response(payment_history, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def generate_invoice_pdf(self, request, pk=None):
        """Générer un PDF de la facture."""
        invoice = self.get_object()
        try:
            pdf_filename = invoice.generate_invoice_pdf()
            return Response({'pdf_file': pdf_filename}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]


class SchoolExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolExpenseSerializer
    permission_classes = [IsAuthenticated, IsManager, IsDirector]
    
    def get_queryset(self):
        """Récupère les frais de scolarité de l'école de l'utilisateur connecté (ou un filtre personnalisé)."""
        return SchoolExpense.objects.filter(school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        """Ajouter l'école de l'utilisateur connecté à la frais de scolarité."""
        serializer.save(school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        """Personnaliser la création pour inclure l'école de l'utilisateur."""
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette frais de scolarité."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette frais de scolarité."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    # Action pour l'historique des dépenses
    @action(detail=False, methods=['get'], url_path='expense-history')
    def expense_history(self, request):
        school = request.user.school_code
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        expenses = SchoolExpense.objects.filter(school=school)

        # Filtrer par date si spécifié
        if start_date:
            expenses = expenses.filter(date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            expenses = expenses.filter(date__lte=datetime.strptime(end_date, '%Y-%m-%d'))

        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)

    # Action pour le suivi global des dépenses
    @action(detail=False, methods=['get'], url_path='total-expenses')
    def total_expenses(self, request):
        school = request.user.school_code
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        expenses = SchoolExpense.objects.filter(school=school)

        # Filtrer par date si spécifié
        if start_date:
            expenses = expenses.filter(date__gte=datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            expenses = expenses.filter(date__lte=datetime.strptime(end_date, '%Y-%m-%d'))

        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "school": school.name,
            "total_expenses": total_expenses,
            "start_date": start_date,
            "end_date": end_date
        })