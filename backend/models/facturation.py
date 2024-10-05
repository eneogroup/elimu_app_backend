from django.db import models
import uuid
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from elimu_app_backend import settings
from backend.constant import months
from django.core.files.base import ContentFile
from weasyprint import HTML
import os

class SchoolInvoice(models.Model):
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey('backend.Pupil', on_delete=models.CASCADE, related_name='Élève')
    school = models.ForeignKey('backend.School', on_delete=models.CASCADE, related_name='École')
    classroom = models.ForeignKey('backend.Classroom', on_delete=models.CASCADE, verbose_name="Salle de classe")
    date = models.DateField(verbose_name='Date de facturation')
    due_date = models.DateField(verbose_name='Date d\'échéance')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant')
    schooling_of = models.CharField(max_length=10, choices=months)
    choices = [('Entièrement payé', 'Entièrement payé'), ('Non payé', 'Non payé'), ('Avance', 'Avance')]
    invoice_status = models.CharField(max_length=20, choices=choices, verbose_name='Statut')
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='Mode de paiement')
    is_recurring = models.BooleanField(default=False, verbose_name='Facture récurrente')
    recurrence_period = models.CharField(max_length=20, blank=True, choices=[('Mensuel', 'Mensuel'), ('Trimestriel', 'Trimestriel'), ('Annuel', 'Annuel')])
    is_active = models.BooleanField(default=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Frais de retard')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Facture {self.invoice_number} - {self.student.lastname}'

    def get_total_paid_amount(self):
        return sum(payment.amount for payment in self.payments.filter(is_paid=True))

    def get_remaining_amount(self):
        return self.amount - self.get_total_paid_amount()

    def get_payment_status(self):
        if self.get_total_paid_amount() >= self.amount:
            return 'Entièrement payé'
        elif self.get_total_paid_amount() > 0:
            return 'Partiellement payé'
        else:
            return 'Non payé'
    
    def send_invoice_email(self):
        """Envoie l'email de la facture au destinataire."""
        subject = f'Facture {self.invoice_number} - {self.student.lastname}'
        html_message = render_to_string('emails/invoice_email.html', {'invoice': self})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER  # L'email de l'expéditeur
        recipient_list = [self.student.email]  # Assurez-vous que l'élève a un champ email

        # Envoi de l'email
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
    
    def generate_invoice_pdf(self):
        # Vérifie si la facture est payée
        if not self.is_paid:
            raise ValueError("La facture n'est pas encore payée. Impossible de générer le PDF.")

        # Récupère les informations de la facture
        context = {
            'invoice': self,
            'student': self.student,
            'classroom': self.classroom,
        }
        
        # Rendre le template HTML pour la facture
        html_string = render_to_string('invoices/invoice_template.html', context)

        # Générer le PDF
        pdf_file = HTML(string=html_string).write_pdf()

        # Enregistrer le PDF dans un fichier (ou dans un stockage)
        pdf_filename = f'invoice_{self.invoice_number}.pdf'
        pdf_file_path = os.path.join('invoices', pdf_filename)  # Spécifie le chemin où tu veux sauvegarder le PDF

        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)

        # Sauvegarder le fichier PDF
        with open(pdf_file_path, 'wb') as f:
            f.write(pdf_file)

        return pdf_filename  # Retourne le nom du fichier PDF généré

    def calculate_late_fees(self):
        if timezone.now().date() > self.due_date:
            return self.late_fee
        return 0

    def mark_as_paid(self, amount):
        self.is_paid = True
        self.save()
        # Optionnel : Enregistrer le paiement ici ou appeler une méthode de paiement

    def get_invoice_summary(self):
        return {
            'invoice_number': str(self.invoice_number),
            'student': self.student.full_name(),
            'amount': self.amount,
            'total_paid': self.get_total_paid_amount(),
            'remaining_amount': self.get_remaining_amount(),
            'due_date': self.due_date,
            'status': self.get_payment_status(),
        }

    class Meta:
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'
        ordering = ['-date']
    
    def get_payment_history(self):
        return [payment.get_payment_details() for payment in self.payments.all()]



class Payment(models.Model):
    invoice = models.ForeignKey(SchoolInvoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Date de paiement')
    payment_method = models.CharField(max_length=50, verbose_name='Mode de paiement')
    is_partial = models.BooleanField(default=False, verbose_name='Paiement partiel')
    reference_number = models.CharField(max_length=50, blank=True, verbose_name='Numéro de référence')
    notes = models.TextField(blank=True, verbose_name='Notes')

    def __str__(self):
        return f'Paiement de {self.amount} pour {self.invoice}'

    def get_payment_details(self):
        return {
            'invoice': str(self.invoice.invoice_number),
            'amount': self.amount,
            'payment_date': self.payment_date,
            'payment_method': self.payment_method,
            'is_partial': self.is_partial,
            'reference_number': self.reference_number,
        }

    def refund_payment(self):
        # Logique pour traiter un remboursement
        pass

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-payment_date']
    



class PaymentTracking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('Terminé', 'Terminé'),
        ('Annulé', 'Annulé'),
    ]

    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='tracking')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='En attente', verbose_name='Statut')
    tracked_date = models.DateTimeField(auto_now_add=True, verbose_name='Date de suivi')
    notes = models.TextField(blank=True, verbose_name='Notes')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')

    def __str__(self):
        return f'Suivi de paiement {self.payment.id} - {self.status}'

    def update_status(self, new_status):
        """Met à jour le statut du paiement suivi."""
        if new_status in dict(self.PAYMENT_STATUS_CHOICES):
            self.status = new_status
            self.save()

    def get_tracking_summary(self):
        """Retourne un résumé des informations de suivi."""
        return {
            'payment_id': self.payment.id,
            'status': self.status,
            'tracked_date': self.tracked_date,
            'notes': self.notes,
        }

    class Meta:
        verbose_name = 'Suivi de paiement'
        verbose_name_plural = 'Suivis de paiements'
        ordering = ['-tracked_date']
