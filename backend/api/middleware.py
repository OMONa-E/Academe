from typing import Any
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import AuditLog
import user_agents, jwt
from rest_framework_simplejwt.tokens import AccessToken

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
        
# Add Role To Token Middlware Class
# ---------------------------------------------------------
class AddRoleToTokenMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the request is to the token endpoint and response is successful
        if request.path == '/api/token/' and response.status_code == 200:
            access_token = response.data.get("access")
            
            if access_token:
                # Decode the token to get the existing payload
                decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])

                # Get the user's role based on the user_id in the token payload
                try:
                    user = User.objects.get(id=decoded_token["user_id"])
                    role = getattr(user, "role", None)

                    # If the user has a role, add it to the token payload
                    if role:
                        # Create a new token with additional claim
                        new_token = AccessToken.for_user(user)
                        new_token['role'] = role
                        
                        # Update the response with the modified token
                        response.data["access"] = str(new_token)
                except User.DoesNotExist:
                    # Log an error or handle the case where the user is not found
                    pass

        return response
    