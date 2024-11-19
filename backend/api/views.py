from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import *
from .serializers import *
from .permissions import *


# Custom TokenObtainPair API View
# ------------------------------------------------------------
@extend_schema(
    description="Obtain an access and refresh token by providing valid credentials.",
    responses={ 200: "Tokens generated successfully", 401: "Invalid credentials" },
    examples=[
        OpenApiExample( name="Valid Request", value={"username": "user", "password": "password"}, request_only=True ),
        OpenApiExample( name="Valid Response", value={"access": "JWT_ACCESS_TOKEN", "refresh": "JWT_REFRESH_TOKEN"}, response_only=True )
    ]
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
# Logout API View
# ------------------------------------------------------------
@extend_schema(
    description="Logout the user by blacklisting their refresh token.",
    request={"refresh": "JWT_REFRESH_TOKEN"},
    responses={ 205: "Successfully logged out", 400: "Invalid refresh token or bad request" }
)
class LogoutView(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request):
        try: 
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [ permissions.IsAdminUser, IsCEO ]

    def perform_create(self, serializer):
        user = serializer.save(role='Employer', is_staff=True)
        EmployeeProfile.objects.create(user=user)

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
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]

@extend_schema(
    description="List all employer profiles.",
    responses={200: EmployerProfileSerializer(many=True)}
)
class EmployerProfileListView(generics.ListAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]

@extend_schema(
    description="Update an employer profile.",
    request=EmployerProfileSerializer,
    responses={200: EmployerProfileSerializer}
)
class EmployerProfileUpdateView(generics.UpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ] 

@extend_schema(
    description="Retrieve details of a specific employee profile.",
    responses={200: EmployeeProfileSerializer}
)
class EmployeeProfileDetailView(generics.RetrieveAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

@extend_schema(
    description="List all employee profiles.",
    responses={200: EmployeeProfileSerializer(many=True)}
)
class EmployeeProfileListView(generics.ListAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

@extend_schema(
    description="Update an employee profile.",
    request=EmployeeProfileSerializer,
    responses={200: EmployeeProfileSerializer}
)
class EmployeeProfileUpdateView(generics.UpdateAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# ------------------------------------------------------------
# Employer - Employee Delete API Views
# ------------------------------------------------------------
@extend_schema(
    description="Delete an employer profile.",
    responses={204: "No Content"}
)
class EmployerProfileDeleteView(generics.DestroyAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsCEO ]

@extend_schema(
    description="Delete an employee profile.",
    responses={204: "No Content"}
)
class EmployeeProfileDeleteView(generics.DestroyAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]


# Client API View
# ------------------------------------------------------------
@extend_schema(
    description="Perform CRUD operations on clients.",
    responses={200: ClientSerializer, 201: ClientSerializer, 204: "No Content"}
)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    filterset_fields = [ 'status', 'assigned_employee', 'payment_status' ]
    search_fields = [ 'first_name', 'last_name', 'email', 'nin' ]

# Training Module API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage training modules.",
    responses={200: TrainingModuleSerializer, 201: TrainingModuleSerializer}
)
class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Payment API View
# ------------------------------------------------------------
@extend_schema(
    description="Handle payments for clients.",
    responses={200: PaymentSerializer, 201: PaymentSerializer}
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Notification API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage user notifications.",
    responses={200: NotificationSerializer, 201: NotificationSerializer}
)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @extend_schema(
        description="Mark a specific notification as read.",
        responses={200: "Notification marked as read"}
    )
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

# Training Session API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage training sessions.",
    responses={200: TrainingSessionSerializer, 201: TrainingSessionSerializer}
)
class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Client Progress API View
# ------------------------------------------------------------
@extend_schema(
    description="Manage client progress in training modules.",
    responses={200: ClientProgressSerializer, 201: ClientProgressSerializer}
)
class ClientProgressViewSet(viewsets.ModelViewSet):
    queryset = ClientProgress.objects.all()
    serializer_class = ClientProgressSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Audit Log API View
# ------------------------------------------------------------
@extend_schema(
    description="Retrieve read-only audit logs.",
    responses={200: AuditLogSerilizer(many=True)}
)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerilizer
    permission_classes = [ IsCEO ]
    filter_backends = [ DjangoFilterBackend, filters.SearchFilter ]
    filterset_fields = [ 'actor', 'action_type' ]
    search_fields = [ 'changes', 'timestamp' ]

# Active Session API View
# ------------------------------------------------------------
@extend_schema(
    description="Retrieve a list of active sessions (login and session updates).",
    responses={200: AuditLogSerilizer(many=True)}
)    
class ActiveSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.filter(action_type__in=['login', 'session_update'])
    serializer_class = AuditLogSerilizer
    permission_classes = [ IsCEO ]