from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'training-module', views.TrainingModuleViewSet)
router.register(r'client-progress', views.ClientProgressViewSet)
router.register(r'training-sessions', views.TrainingSessionViewSet)

urlpatterns = [
    # Viewset URL
    path('', include(router.urls)),
    # Registration URLs
    path('register/employer/', views.EmployerRegistrationView.as_view(), name='employer-register'), # Create
    path('register/employee/', views.EmployeeResgistrationView.as_view(), name='employee-register'), # Create
]

urlpatterns += [
    # Employer URLs
    path('employers/', views.EmployerProfileListView.as_view(), name='employer-list'),               # List
    path('employers/<int:pk>/', views.EmployerProfileDetailView.as_view(), name='employer-detail'),  # Retrieve
    path('employers/<int:pk>/update/', views.EmployerProfileUpdateView.as_view(), name='employer-update'),  # Update
    path('employers/<int:pk>/delete/', views.EmployerProfileDeleteView.as_view(), name='employer-delete'),  # Delete

    # Employee URLs
    path('employees/', views.EmployeeProfileListView.as_view(), name='employee-list'),                # List
    path('employees/<int:pk>/', views.EmployeeProfileDetailView.as_view(), name='employee-detail'),   # Retrieve
    path('employees/<int:pk>/update/', views.EmployeeProfileUpdateView.as_view(), name='employee-update'),  # Update
    path('employees/<int:pk>/delete/', views.EmployeeProfileDeleteView.as_view(), name='employee-delete'),  # Delete
]

