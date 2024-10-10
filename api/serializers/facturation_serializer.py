from backend.models.facturation import ExpenseCategory, Payment, PaymentTracking, SchoolExpense, SchoolInvoice
from rest_framework import serializers

class SchoolInvoiceSerializer(serializers.ModelSerializer):
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    payment_status = serializers.CharField(source='get_payment_status', read_only=True)
    late_fees = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = SchoolInvoice
        fields = [
            'id', 'invoice_number', 'is_paid', 'student', 'school', 'classroom', 'date', 'due_date',
            'amount', 'schooling_of', 'invoice_status', 'payment_method', 'is_recurring',
            'recurrence_period', 'is_active', 'late_fee', 'created_at', 'updated_at',
            'total_paid', 'remaining_amount', 'payment_status', 'late_fees'
        ]



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentTrackingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = PaymentTracking
        fields = '__all__'


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class SchoolExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolExpense
        fields = '__all__'

