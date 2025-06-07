# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, LoginSerializer
from .models import Account
from django.contrib.auth.hashers import check_password

class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({
                    "success": False,
                    "error": "Invalid email or password."
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not check_password(password, account.password):
                return Response({
                    "success": False,
                    "error": "Invalid email or password."
                }, status=status.HTTP_401_UNAUTHORIZED)

            # Optional: Check if staff is active/approved
            if account.role == 'staff':
                if not account.is_approved or not account.is_active_staff:
                    return Response({
                        "success": False,
                        "error": "Staff not approved or deactivated."
                    }, status=status.HTTP_403_FORBIDDEN)

            # ✅ Successful login
            user_data = {
                "email": account.email,
                "username": account.username,
                "role": account.role
            }
            return Response({
                "user": user_data
            }, status=status.HTTP_200_OK)

        # Validation errors
        return Response({
            "success": False,
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    def get(self, request):
        users = Account.objects.all()
        serializer = AccountSerializer(users, many=True)
        return Response({
            "total_users": users.count(),
            "users": serializer.data
        }, status=status.HTTP_200_OK)
