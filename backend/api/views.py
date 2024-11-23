from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .models import *
from .serializers import *
from .permissions import *


# Default View
# ------------------------------------------------------------
def welcome_view(request):
    return render(request, 'welcome.html')

# Custom TokenObtainPair API View
# ------------------------------------------------------------
@extend_schema(
    description="Obtain an access and refresh token by providing valid credentials.",
    responses={
        200: OpenApiResponse(
            description="Tokens generated successfully.",
            examples=[
                OpenApiExample(
                    name="Successful Token Generation",
                    value={"access": "JWT_ACCESS_TOKEN", "refresh": "JWT_REFRESH_TOKEN"}
                )
            ]
        ),
        401: OpenApiResponse(
            description="Invalid credentials provided.",
            examples=[
                OpenApiExample(
                    name="Invalid Credentials",
                    value={"detail": "No active account found with the given credentials"}
                )
            ]
        )
    }
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
# Logout API View
# ------------------------------------------------------------
@extend_schema(
    description="Logout the user by blacklisting their refresh token.",
    request=LogoutRequestSerializer,
    responses={
        205: OpenApiResponse(description="Successfully logged out"),
        400: OpenApiResponse(description="Invalid refresh token or bad request")
    }
)
class LogoutView(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        try: 
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Employer Registration API View
# ------------------------------------------------------------
@extend_schema(
    description="Register a new employer user.",
    request=CustomUserSerializer,
    responses={201: EmployerProfileSerializer}
)
class EmployerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role='Employer')
    serializer_class = CustomUserSerializer
    permission_classes = [ IsCEO ]

    def perform_create(self, serializer):
        user = serializer.save(role='Employer', is_staff=True)
        EmployerProfile.objects.create(user=user)

# Employee Registration API View
# ------------------------------------------------------------
@extend_schema(
    description="Register a new employee user.",
    request=CustomUserSerializer,
    responses={201: EmployeeProfileSerializer}
)
class EmployeeResgistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role='Employee')
    serializer_class = CustomUserSerializer
    permission_classes = [ IsEmployerOrCEO ]

    def perform_create(self, serializer):
        user = serializer.save(role='Employee', is_staff=True)
        EmployeeProfile.objects.create(user=user)

# ------------------------------------------------------------
# Employer - Employee ReadUpdateList API Views
# ------------------------------------------------------------
@extend_schema(
    description="Retrieve details of a specific employer profile.",
    responses={200: EmployerProfileSerializer}
)
class EmployerProfileDetailView(generics.RetrieveAPIView):
    queryset = EmployerProfile.objects.select_related('user')
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]

@extend_schema(
    description="List all employer profiles.",
    responses={200: EmployerProfileSerializer(many=True)}
)
class EmployerProfileListView(generics.ListAPIView):
    queryset = EmployerProfile.objects.select_related('user')
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]

@extend_schema(
    description="Update an employer profile.",
    request=EmployerProfileSerializer,
    responses={200: EmployerProfileSerializer}
)
class EmployerProfileUpdateView(generics.UpdateAPIView):
    queryset = EmployerProfile.objects.select_related('user')
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ] 

@extend_schema(
    description="Retrieve details of a specific employee profile.",
    responses={200: EmployeeProfileSerializer}
)
class EmployeeProfileDetailView(generics.RetrieveAPIView):
    queryset = EmployeeProfile.objects.select_related('user', 'employer')
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

@extend_schema(
    description="List all employee profiles.",
    responses={200: EmployeeProfileSerializer(many=True)}
)
class EmployeeProfileListView(generics.ListAPIView):
    queryset = EmployeeProfile.objects.select_related('user', 'employer')
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

@extend_schema(
    description="Update an employee profile.",
    request=EmployeeProfileSerializer,
    responses={200: EmployeeProfileSerializer}
)
class EmployeeProfileUpdateView(generics.UpdateAPIView):
    queryset = EmployeeProfile.objects.select_related('user', 'employer')
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# ------------------------------------------------------------
# Employer - Employee Delete API Views
# ------------------------------------------------------------
@extend_schema(
    description="Delete an employer profile.",
    responses={204: OpenApiResponse(description="Employer profile successfully deleted.")}
)
class EmployerProfileDeleteView(generics.DestroyAPIView):
    queryset = EmployerProfile.objects.select_related('user')
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsCEO]

@extend_schema(
    description="Delete an employee profile.",
    responses={204: OpenApiResponse(description="Employee profile successfully deleted.")}
)
class EmployeeProfileDeleteView(generics.DestroyAPIView):
    queryset = EmployeeProfile.objects.select_related('user', 'employer')
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsEmployerOrCEO]


# Client API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage client records.",
    responses={200: ClientSerializer(many=True), 201: ClientSerializer, 204: OpenApiResponse(description="No Content")}
)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related('assigned_employee__user')
    serializer_class = ClientSerializer
    permission_classes = [IsEmployerOrEmployeeOrCEO]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'assigned_employee', 'payment_status']
    search_fields = ['first_name', 'last_name', 'email', 'nin']

    @extend_schema(operation_id="clients_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="clients_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="clients_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="clients_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="clients_partial_update")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="clients_delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Training Module API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage training modules.",
    responses={200: TrainingModuleSerializer(many=True), 201: TrainingModuleSerializer, 204: OpenApiResponse(description="No Content")}
)
class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @extend_schema(operation_id="training_modules_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="training_modules_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="training_modules_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="training_modules_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="training_modules_partial_update")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="training_modules_delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Payment API View
# ------------------------------------------------------------
@extend_schema(
    description="Handle payments for clients.",
    responses={200: PaymentSerializer(many=True), 201: PaymentSerializer, 204: OpenApiResponse(description="No Content")}
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @extend_schema(operation_id="payments_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="payments_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="payments_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="payments_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="payments_partial_update")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="payments_delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Notification API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage user notifications.",
    responses={200: NotificationSerializer(many=True), 201: NotificationSerializer, 204: OpenApiResponse(description="No Content")}
)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @extend_schema(
        description="Mark a specific notification as read.",
        responses={200: OpenApiResponse(description="Notification marked as read")}
    )
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        try:
            notification = self.get_object()
            notification.is_read = True
            notification.save()
            return Response({'status': 'Notification marked as read'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(operation_id="notifications_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="notifications_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="notifications_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="notifications_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="notifications_partial_update")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="notifications_delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Training Session API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage training sessions.",
    responses={200: TrainingSessionSerializer(many=True), 201: TrainingSessionSerializer, 204: OpenApiResponse(description="No Content")}
)
class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @extend_schema(operation_id="training_sessions_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="training_sessions_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="training_sessions_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="training_sessions_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="training_sessions_partial_update")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="training_sessions_delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Client Progress API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage client progress in training modules.",
    responses={200: ClientProgressSerializer(many=True), 201: ClientProgressSerializer, 204: OpenApiResponse(description="No Content")}
)
class ClientProgressViewSet(viewsets.ModelViewSet):
    queryset = ClientProgress.objects.all()
    serializer_class = ClientProgressSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @extend_schema(operation_id="client_progresses_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="client_progresses_create")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(operation_id="client_progresses_retrieve")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(operation_id="client_progresses_update")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(operation_id="client_progresses_partial_update")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(operation_id="client_progresses_delete")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Audit Log API View
# ------------------------------------------------------------
@extend_schema(
    description="Retrieve all audit logs."
)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerilizer
    permission_classes = [IsCEO]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['actor', 'action_type']
    search_fields = ['changes', 'timestamp']

    @extend_schema(operation_id="audit_logs_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="audit_logs_detail")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

# Active Session API View
# ------------------------------------------------------------
@extend_schema(
    description="Retrieve a list of active sessions (login and session updates)."
)
class ActiveSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.filter(action_type__in=['login', 'session_update'])
    serializer_class = AuditLogSerilizer
    permission_classes = [IsCEO]

    @extend_schema(operation_id="active_sessions_list")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(operation_id="active_sessions_detail")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
