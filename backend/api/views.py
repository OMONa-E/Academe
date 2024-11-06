from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *


# Employer Registration API View
# ------------------------------------------------------------
class EmployerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.filter(role='Employer')
    serializer_class = CustomUserSerializer
    permission_classes = [ permissions.IsAdminUser, IsCEO ]

    def perform_create(self, serializer):
        user = serializer.save(role='Employer', is_staff=True)
        EmployeeProfile.objects.create(user=user)

# Employee Registration API View
# ------------------------------------------------------------
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
class EmployerProfileDetailView(generics.RetrieveAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]

class EmployerProfileListView(generics.ListAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]

class EmployerProfileUpdateView(generics.UpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsEmployerOrCEO ] 

class EmployeeProfileDetailView(generics.RetrieveAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

class EmployeeProfileListView(generics.ListAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

class EmployeeProfileUpdateView(generics.UpdateAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# ------------------------------------------------------------
# Employer - Employee Delete API Views
# ------------------------------------------------------------
class EmployerProfileDeleteView(generics.DestroyAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [ IsCEO ]

class EmployeeProfileDeleteView(generics.DestroyAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer
    permission_classes = [ IsEmployerOrCEO ]


# Client API View
# ------------------------------------------------------------
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Training Module API View
# ------------------------------------------------------------
class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.all()
    serializer_class = TrainingModuleSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Payment API View
# ------------------------------------------------------------
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Notification API View
# ------------------------------------------------------------
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

# Training Session API View
# ------------------------------------------------------------
class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]

# Client Progress API View
# ------------------------------------------------------------
class ClientProgressViewSet(viewsets.ModelViewSet):
    queryset = ClientProgress.objects.all()
    serializer_class = ClientProgressSerializer
    permission_classes = [ IsEmployerOrEmployeeOrCEO ]
