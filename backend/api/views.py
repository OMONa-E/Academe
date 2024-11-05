from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


# Employer Registration API View
# ------------------------------------------------------------
class EmployerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role='Employer')
    serializer_class = CustomUserSerializer
    permission_classes = [ permissions.IsAdminUser ]

    def perform_create(self, serializer):
        user = serializer.save(role='Employer', is_staff=True)
        EmployeeProfile.objects.create(user=user)

# Employee Registration API View
# ------------------------------------------------------------
class EmployeeResgistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role='Employee')
    serializer_class = CustomUserSerializer
    permission_classes = [ permissions.IsAuthenticated ]

    def perform_create(self, serializer):
        user = serializer.save(role='Employee', is_staff=True)
        EmployeeProfile.objects.create(user=user)
        
# Client API View
# ------------------------------------------------------------
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ IsAuthenticated ]

# Training Module API View
# ------------------------------------------------------------
class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer
    permission_classes = [ IsAuthenticated ]

# Payment API View
# ------------------------------------------------------------
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [ IsAuthenticated ]

# Notification API View
# ------------------------------------------------------------
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [ IsAuthenticated ]

# Training Session API View
# ------------------------------------------------------------
class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [ IsAuthenticated ]

# Client Progress API View
# ------------------------------------------------------------
class ClientProgressViewSet(viewsets.ModelViewSet):
    queryset = ClientProgress.objects.all()
    serializer_class = ClientProgressSerializer
    permission_classes = [ IsAuthenticated ]
