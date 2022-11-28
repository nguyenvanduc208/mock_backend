from rest_framework import serializers

from .models import RoomOrder


class RoomOrderSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source='user.full_name')

    class Meta:
        model = RoomOrder
        fields = ['room_name', 'start_time', 'end_time', 'user_fullname']
        read_only_fields = ['user_fullname']
