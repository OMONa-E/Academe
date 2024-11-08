from typing import Any
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import AuditLog
import user_agents

# Initialize our User model
# ---------------------------------------------------------
User = get_user_model()

# Session Tracking Middlware Class
# ---------------------------------------------------------
class SessionTrackingMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
    
    def __call__(self, request) -> Any:
        response = self.get_response(request)

        if request.user.is_authenticated:
            ip_address = request.META.get('REMOTE_ADDR') # Retrieve IP Address
            # Retrieve User-Agent and parse device info
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            parsed_ua = user_agents.parse(user_agent)
            device_info = f'{parsed_ua.device} on {parsed_ua.os} using {parsed_ua.browser}'

            log_entry, created = AuditLog.objects.get_or_create( # Update or create the AuditLog entry for session tracking
                actor=request.user,
                target_model='CustomUser',
                target_object_id=request.user.id,
                defaults={
                    'action_type': 'login',
                    'changes': {},
                    'login_timestamp': timezone.now(),
                    'ip_address': ip_address,
                    'device_info': device_info
                }
            )
            if not created:
                log_entry.action_type = 'session_update'
                log_entry.last_active = timezone.now() # Update the last active timestamp on every request
                log_entry.save()
        return response
        