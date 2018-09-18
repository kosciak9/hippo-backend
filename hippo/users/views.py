from django_filters.rest_framework import DjangoFilterBackend
from hippo.users.models import Availability, Position, Team, User
from hippo.users.serializers import (AvailabilitySerializer,
                                     PositionSerializer, TeamSerializer,
                                     UserSerializer)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class AvailabilityViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives user availablity
    """
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('date', 'time', 'player', )


class TeamViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', )


class PositionViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives positions
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('name', )


class UserViewSet(viewsets.ModelViewSet):
    """
    Updates and retrives user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('username', )
