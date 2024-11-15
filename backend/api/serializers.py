from typing import Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, any]) -> Dict[str, str]:
        data = super().validate(attrs)

        user = self.user # get user instance
        data['role'] = user.role if hasattr(user, 'role') else None # validate and add role to the token response data

        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [ 'id', 'username', 'email', 'first_name', 'last_name', 'role', 'date_of_birth', 'nin' ]
        extra_kwargs = {'password': {'write_only': True}}

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
        extra_kwargs = {'employer': {'read_only': True}}

class ClientSerializer(serializers.ModelSerializer):
    assigned_employee = EmployeeProfileSerializer()
    class Meta:
        model = models.Client
        fields = [ 'id', 'first_name', 'last_name', 'email', 'nin', 'phone_number', 'status', 'assigned_employee', 'payment_status' ]

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
        extra_kwargs = {'client': {'read_only': True}, 'module': {'read_only': True}}

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
       extra_kwargs = {'client': {'read_only': True}} 

class NotificationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = models.Notification
        fields = [ 'id', 'user', 'message', 'created_at', 'is_read' ]
        extra_kwargs = {'user': {'read_only': True}}

class AuditLogSerilizer(serializers.ModelSerializer):
    actor = CustomUserSerializer()
    class Meta:
        model = models.AuditLog
        fields = [ 'id', 'action_type', 'timestamp', 'actor', 'target_model', 'target_object_id', 'changes' ]
