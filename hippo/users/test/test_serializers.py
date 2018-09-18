from django.forms.models import model_to_dict
from django.test import TestCase
from nose.tools import eq_, ok_

from hippo.users.serializers import (AvailabilitySerializer,
                                     PositionSerializer, TeamSerializer,
                                     UserSerializer)
from hippo.users.test.factories import (AdditionalPerkFactory,
                                        AvailabilityFactory, PositionFactory,
                                        TeamFactory, UserFactory)


class TestUserSerializer(TestCase):

    def setUp(self):
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = UserSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = UserSerializer(data=self.user_data)
        ok_(serializer.is_valid())


class TestPositionSerializer(TestCase):

    def setUp(self):
        self.position_data = model_to_dict(PositionFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = PositionSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = PositionSerializer(data=self.position_data)
        ok_(serializer.is_valid())


class TestTeamSerializer(TestCase):

    def setUp(self):
        self.admin_perk = AdditionalPerkFactory.create()
        self.team_data = model_to_dict(TeamFactory.build(
            admin_perk=self.admin_perk
        ))

    def test_serializer_with_empty_data(self):
        serializer = TeamSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = TeamSerializer(data=self.team_data)
        serializer.is_valid()
        ok_(serializer.is_valid())


class TestAvailabilitySerializer(TestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.availability_data = model_to_dict(AvailabilityFactory.build(
            player=self.user
        ))

    def test_serializer_with_empty_data(self):
        serializer = AvailabilitySerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = AvailabilitySerializer(data=self.availability_data)
        ok_(serializer.is_valid())
