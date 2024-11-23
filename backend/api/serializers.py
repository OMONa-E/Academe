from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_field
from . import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        token['email'] = user.email
        
        print(f'Token generated for user: {user.username}')
        return token

class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.CustomUser
        fields = [ 'id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role', 'date_of_birth', 'nin' ] 
    
    def validate(self, attrs): # validates password and password2 equality
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs
    
    def create(self, validated_data): # remove password2 since it's not part of the model; create the user and hash the password
        validated_data.pop('password2')
        user = models.CustomUser.objects.create_user(**validated_data)
        return user

class EmployerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    class Meta:
        model = models.EmployerProfile
        fields = [ 'username', 'email', 'first_name', 'last_name', 'role', 'department', ]

class EmployeeProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True) 

    employer = EmployerProfileSerializer(read_only=True)
    class Meta:
        model = models.EmployeeProfile
        fields = [ 'username', 'email', 'first_name', 'last_name', 'role', 'department', 'employer', ]

class ClientSerializer(serializers.ModelSerializer):
    assigned_employee = serializers.SerializerMethodField()

    class Meta:
        model = models.Client
        fields = [
            'id', 'first_name', 'last_name', 'email', 'nin', 'phone_number',
            'status', 'assigned_employee', 'payment_status'
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_assigned_employee(self, obj) -> str:
        """
        Resolve the assigned employee's username.
        """
        if obj.assigned_employee and obj.assigned_employee.user:
            return obj.assigned_employee.user.username
        return None

    def validate(self, attrs):
        """
        Validate and handle default assignment of `assigned_employee` if not provided.
        """
        request = self.context.get('request')
        if not attrs.get('assigned_employee'):
            if request and hasattr(request.user, 'employeeprofile'):
                # Default to the current user’s employee profile if the user is an employee
                attrs['assigned_employee'] = request.user.employeeprofile
            else:
                # Default to the first available employee profile
                default_employee = models.EmployeeProfile.objects.first()
                if default_employee:
                    attrs['assigned_employee'] = default_employee
                else:
                    raise serializers.ValidationError({
                        'assigned_employee': 'No assigned employee provided, and no default available.'
                    })
        return attrs

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
    actor = serializers.SerializerMethodField()
    class Meta:
        model = models.AuditLog
        fields = [ 'id', 'action_type', 'timestamp', 'actor', 'target_model', 'target_object_id', 'changes' ]

    @extend_schema_field(CustomUserSerializer)
    def get_actor(self, obj):
        if obj.actor:
            return CustomUserSerializer(obj.actor).data
        return None
