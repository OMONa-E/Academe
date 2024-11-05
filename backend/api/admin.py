from django.contrib import admin
from .models import *

# Register your models here. 
admin.site.register( (CustomUser, EmployeeProfile, EmployerProfile, Client) )
admin.site.register( (TrainingModule, ClientProgress, TrainingSession, Payment, Notification, AuditLog) )
