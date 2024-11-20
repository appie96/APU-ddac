from rest_framework import serializers
from .models import Reservation, Menu, User  # Use custom User model

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'email', 'date', 'time', 'guests', 'status', 'created_at']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'image_url', 'category', 'is_available']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'username']
        read_only_fields = ['id', 'email']
