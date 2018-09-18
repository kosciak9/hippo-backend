from hippo.users.models import Availability, Position, Team, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'kit_number', 'position', 'team', 'locale', )
        read_only_fields = ('auth_token',)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('pk', 'name', )


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('pk', 'name', 'admin_perk',
                  'hour_count', 'hours',
                  'days_to_fill_ahead_certain',
                  'days_to_fill_ahead_approximate', )


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('date', 'available', 'approximate_available',
                  'player', 'edited', )
