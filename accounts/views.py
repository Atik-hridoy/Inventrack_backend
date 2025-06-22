# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, LoginSerializer, UserProfileSerializer, UserProfileEditHistorySerializer
from .models import Account, UserProfileEditHistory
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

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
                "id": account.id,  # Include user id here
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
    permission_classes = []  # Allow any user (no authentication required)

    def get(self, request):
        return Response({'error': 'Unauthorized: Please log in to view your profile.'}, status=401)

    def put(self, request):
        return Response({'error': 'Unauthorized: Please log in to update your profile.'}, status=401)

    def patch(self, request):
        return self.put(request)

class UserProfileEditHistoryView(APIView):
    permission_classes = []  # Allow any user (no authentication required)
    def get(self, request):
        return Response({'error': 'Access denied. Only admin can view edit history.'}, status=403)
    def post(self, request):
        required_fields = ['user_id']
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=400)
        from .models import Account
        try:
            account = Account.objects.get(id=user_id, role='user')
        except Account.DoesNotExist:
            return Response({'error': 'User not found or not a user.'}, status=404)
        # Compare and update all profile fields
        changed_fields = []
        for field in ['phone', 'nickname', 'address_street', 'address_house', 'address_district']:
            if field in request.data:
                old_value = getattr(account, field, None)
                new_value = request.data[field]
                if old_value != new_value:
                    setattr(account, field, new_value)
                    changed_fields.append((field, old_value, new_value))
        account.save()
        # Save edit history for each changed field
        for field, old_value, new_value in changed_fields:
            UserProfileEditHistory.objects.create(
                user=account,
                field_changed=field,
                old_value=old_value,
                new_value=new_value
            )
        return Response({'message': 'Profile updated and history saved.', 'changes': changed_fields}, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes = []
    def get(self, request):
        users = Account.objects.filter(is_superuser=False)
        serializer = AccountSerializer(users, many=True)
        return Response({
            "total_users": users.count(),
            "users": serializer.data
        }, status=status.HTTP_200_OK)
