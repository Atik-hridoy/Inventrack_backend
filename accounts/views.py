# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, LoginSerializer, UserProfileSerializer
from .models import Account
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    permission_classes = []  # <-- No authentication required

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []  # <-- No authentication required
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response({"success": False, "error": "Invalid email or password."}, status=401)

            if not check_password(password, account.password):
                return Response({"success": False, "error": "Invalid email or password."}, status=401)

            if account.role == 'staff' and not account.is_approved:
                return Response({"success": False, "error": "Staff not approved by admin."}, status=403)

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
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user
        serializer = AccountSerializer(account)
        return Response(serializer.data)


class UserListView(APIView):
    permission_classes = []
    def get(self, request):
        users = Account.objects.filter(is_superuser=False)
        serializer = AccountSerializer(users, many=True)
        return Response({
            "total_users": users.count(),
            "users": serializer.data
        }, status=status.HTTP_200_OK)
