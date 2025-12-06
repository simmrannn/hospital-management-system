from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import DoctorProfile, PatientProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_doctor', 'is_patient')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['doctor', 'patient'])
    specialization = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'specialization', 'address')

    def create(self, validated_data):
        role = validated_data.pop('role')
        specialization = validated_data.pop('specialization', '')
        address = validated_data.pop('address', '')
        
        is_doctor = role == 'doctor'
        is_patient = role == 'patient'
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_doctor=is_doctor,
            is_patient=is_patient
        )
        
        if is_doctor:
            DoctorProfile.objects.create(user=user, specialization=specialization)
        elif is_patient:
            PatientProfile.objects.create(user=user, address=address)
            
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
