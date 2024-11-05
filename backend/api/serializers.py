from rest_framework import serializers
from . import models


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [ 'id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_of_birth', 'nin' ]

class EmployerProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = models.EmployerProfile
        fields = [ 'user', 'department' ]

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    employer = EmployerProfileSerializer()
    class Meta:
        model = models.EmployeeProfile
        fields = [ 'user', 'department', 'employer' ]

class ClientSerializer(serializers.ModelSerializer):
    assigned_employee = EmployeeProfileSerializer()
    class Meta:
        model = models.Client
        fields = [ 'id', 'first_name', 'last_name', 'email', 'phone_number', 'status', 'assigned_employee', 'payment_status' ]

class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrainingModule
        fields = [ 'id', 'title', 'description', 'duration_hours' ]

class ClientProgressSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    module = TrainingModuleSerializer()
    class Meta:
        model = models.ClientProgress
        fields = [ 'id', 'client', 'module', 'completion_status', 'progress_notes', 'completion_date' ]

class TrainingSessionSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    trainer = EmployeeProfileSerializer()
    class Meta:
        model = models.TrainingSession
        fields = [ 'id', 'client', 'trainer', 'module', 'session_date', 'status', 'notes' ]

class PaymentSerializer(serializers.ModelSerializer):
   client = ClientSerializer()
   class Meta:
       model = models.Payment
       fields = [ 'id', 'client', 'amount', 'payment_date', 'receipt_number' ] 

class NotificationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = models.Notification
        fields = [ 'id', 'user', 'message', 'created_at', 'is_read' ]

class AuditLogSerilizer(serializers.ModelSerializer):
    actor = CustomUserSerializer()
    class Meta:
        model = models.AuditLog
        fields = [ 'id', 'action_type', 'timestamp', 'actor', 'target_model', 'target_object_id', 'changes' ]
