from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



# Custom User Model
# ------------------------------------------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('CEO', 'CEO'),
        ('Employer', 'Employer'),
        ('Employee', 'Employee'),
        # ('Client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    nin = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.username} - ({self.role})"
    
    def save(self, *args, **kwargs):
        if self.role == 'CEO' and not self.is_superuser:
            raise ValueError('CEO roel must be assigned to a superuser.')
        super().save(*args, **kwargs)


# Employer Profile Model
# ------------------------------------------------------------
class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Employer'})
    department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"Employer Profile for {self.user.username}"
    
# Employee Profile Model
# ------------------------------------------------------------
class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'Emplopyee'})
    department = models.CharField(max_length=100, null=True, blank=True)
    employer = models.ForeignKey(EmployerProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"Employee Profile for {self.user.username}"

# Client Model
# ------------------------------------------------------------
class Client(models.Model):
    STATUS_CHOICES = [
        ('partial', 'Partial Registration'),
        ('full', 'Fully Registered'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nin = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='partial')
    assigned_employee = models.ForeignKey(EmployeeProfile, on_delete=models.SET_NULL, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)


# Training Module Model
# ------------------------------------------------------------
class TrainingModule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_hours = models.PositiveIntegerField()

# Client Progress Tracking Model
# ------------------------------------------------------------
class ClientProgress(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completion_status = models.BooleanField(default=False)
    progress_notes = models.TextField(blank=True, null=True)
    completion_date = models.DateTimeField(null=True, blank=True)

# Training Session Management Model
# ------------------------------------------------------------
class TrainingSession(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trainer = models.ForeignKey(EmployeeProfile, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(TrainingModule, on_delete=models.SET_NULL, null=True)
    session_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='scheduled')
    notes = models.TextField(blank=True, null=True)

# Payment Model
# ------------------------------------------------------------
class Payment(models.Model):
    PAY_METHODS = [
        ('MoMo', 'Mobile Money'),
        ('AirtelMoney', 'Airtel Money'),
        ('VisaCard', 'Visa Card'),
        ('Bank', 'Bank Counter')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    receipt_number = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=15, choices=PAY_METHODS, default='MoMo')

# Notification For System Users Model
# ------------------------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# Audit Logs For Activity Tracking Model
# ------------------------------------------------------------
class AuditLog(models.Model):
    action_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    target_model = models.CharField(max_length=100)
    target_object_id = models.PositiveIntegerField()
    changes = models.JSONField()



# Signals To Auto-Generate User Profile and Audit Logs
# ------------------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

# Signal to automatically create Employer or Employee profiles upon user save
@receiver(post_save, sender=CustomUser)
def create_role_based_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'Employer':
            EmployerProfile.objects.get_or_create(user=instance)
        elif instance.role == 'Employee':
            EmployeeProfile.objects.get_or_create(user=instance)

# Signal to log Chnages for audit logs
@receiver(post_save, sender=Client)
@receiver(post_save, sender=TrainingSession)
@receiver(post_save, sender=Payment)
def create_audit_log(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    changes = {field.name: getattr(instance, field.name) for field in instance._meta.fields}
    AuditLog.objects.create(
        action_type=action,
        actor=instance.assigned_employee.user if hasattr(instance, 'assigned_employee') else None,  
        target_model=sender.__name__,
        target_object_id=instance.id,
        changes=changes,
    )
