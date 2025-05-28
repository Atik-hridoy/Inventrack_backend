# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AccountSerializer, LoginSerializer
from .models import Account
from django.contrib.auth.hashers import make_password, check_password

class RegisterView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password
            password = serializer.validated_data['password']
            serializer.validated_data['password'] = make_password(password)

            # Save the user with hashed password and role
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
                if check_password(password, account.password):
                    return Response({
                        "message": "Login successful.",
                        "email": account.email,
                        "role": account.role  # Return role here
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            except Account.DoesNotExist:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
