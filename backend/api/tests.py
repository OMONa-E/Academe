from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Client, TrainingModule, ClientProgress, TrainingSession


# User Tests 
# --------------------------------------------
class UserTests(APITestCase):
    def setUp(self) -> None:
        self.roles = ['CEO', 'Employer', 'Employee']
        self.users = {}
        self.tokens = {}

        # Dynamically create users for all roles and store thier tokens
        for role in self.roles:
            user = CustomUser.objects.create_user(
                username=role.lower(),
                password='password',
                role=role,
                is_superuser=(role == 'CEO')
            )
            self.users[role] = user
            self.tokens[role] = self.get_token_for_user(user)

    def get_token_for_user(self, user):
        '''Generate an access token for a user.'''
        refresh = RefreshToken.for_user(user=user)
        return str(refresh.access_token)
    
    def test_login(self):
        '''Test login for all roles.'''
        url = reverse('token-obtain-pair')
        for role in self.roles:
            with self.subTest(role=role):
                data = { 'username': role.lower(), 'password': 'password' }
                response = self.client.post(url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK, f'Failed for role: {role}')
                self.assertIn('access', response.data, f'Accesss token missing for role: {role}')

    def tets_logout(self):
        '''Test logout for all roles'''
        url = reverse('logout')
        for role in self.roles:
            with self.subTest(role=role):
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens[role]}')
                refresh_token = str(RefreshToken.for_user(self.users[role]))
                response = self.client.post(url, {'refresh': refresh_token}, format='json')
                self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT, f'Failed for role {role}')

# Client Tests 
# --------------------------------------------
class ClientTests(APITestCase):
    def setUp(self) -> None:
        self.roles = ['Employee', 'Employer', 'CEO']
        self.users = {}
        self.tokens = {}

        # Dynamically create users for each role and store their tokens
        for role in self.roles:
            user = CustomUser.objects.create_user(
                username=role.lower(),
                password="password",
                role=role,
                is_superuser=(role == 'CEO')  # Only the CEO is a superuser
            )
            self.users[role] = user
            self.tokens[role] = self.get_token_for_user(user)

        # Initial data for testing
        self.test_client_data = {
            "first_name": "uganda",
            "last_name": "client",
            "nin": "1234567890",
            "email": "uganda.client@test.com",
            "phone_number": "1234567890",
            "status": "partial"
        }

    def get_token_for_user(self, user):
        """Generate an access token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_client(self):
        """Test creating a client for different roles."""
        url = reverse('client-list')
        for role in self.roles:
            with self.subTest(role=role):
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens[role]}')
                response = self.client.post(url, self.test_client_data, format='json')

                if role in ['CEO', 'Employer', 'Employee']:  # Employees should be able to create clients
                    self.assertEqual(response.status_code, status.HTTP_201_CREATED, f"Failed for role: {role}")
                    self.assertEqual(Client.objects.count(), 1)
                    Client.objects.all().delete()  # Clean up after each test
                else:  # Other roles shouldn't be allowed to create clients
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, f"Failed for role: {role}")

    def test_get_client_list(self):
        """Test retrieving the client list for different roles."""
        url = reverse('client-list')
        for role in self.roles:
            with self.subTest(role=role):
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tokens[role]}')
                response = self.client.get(url, format='json')

                if role in ['Employee', 'CEO', 'Employer']:  # Employees and CEOs should have access to the client list
                    self.assertEqual(response.status_code, status.HTTP_200_OK, f"Failed for role: {role}")
                else:  # Other roles shouldn't have access
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, f"Failed for role: {role}")
