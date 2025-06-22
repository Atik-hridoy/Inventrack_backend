from rest_framework import serializers
from .models import Account, UserProfileEditHistory
from django.contrib.auth.hashers import make_password

class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = [
            'id', 'email', 'username', 'password', 'confirm_password', 'role',
            'phone', 'nickname', 'address_street', 'address_house', 'address_district'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'role': {'default': 'user'},
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        role = validated_data.get('role', 'user')
        if role == 'staff':
            validated_data['is_approved'] = False
            validated_data['is_active_staff'] = False
        elif role == 'user':
            validated_data['is_approved'] = True
            validated_data['is_active_staff'] = True
        # Always use the model manager to create the user
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 'email', 'username', 'role',
            'phone', 'nickname', 'address_street', 'address_house', 'address_district'
        ]
        read_only_fields = ['id', 'email', 'username', 'role']


class UserProfileEditHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileEditHistory
        fields = ['id', 'user', 'edited_at', 'field_changed', 'old_value', 'new_value']
        read_only_fields = fields

