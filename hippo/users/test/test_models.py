from freezegun import freeze_time
from datetime import datetime

from django.test import TestCase
from nose.tools import eq_, ok_

from hippo.users.test.factories import (AdditionalPerkFactory,
                                        AvailabilityFactory, PositionFactory,
                                        TeamFactory, UserFactory)


class TestPositionModel(TestCase):
    def test_position_creation(self):
        position = PositionFactory.create()
        eq_(position.pk, 1)

    def test_position_str(self):
        position = PositionFactory.create()
        eq_(position.name, str(position))


class TestAdditionalPerksModel(TestCase):
    def test_perk_creation(self):
        perk = AdditionalPerkFactory.create()
        eq_(perk.pk, 1)

    def test_perk_str(self):
        perk = AdditionalPerkFactory.create()
        eq_(perk.name, str(perk))


class TestUserModel(TestCase):
    def test_user_creation(self):
        user = UserFactory.create()
        ok_(user.id)
        ok_(user.auth_token)

    def test_user_str(self):
        user = UserFactory.create()
        eq_(user.username, str(user))


class TestTeamModel(TestCase):
    def test_team_creation(self):
        team = TeamFactory.create()
        eq_(team.pk, 1)

    def test_team_str(self):
        team = TeamFactory.create()
        eq_(team.name, str(team))


class TestAvailabilityModel(TestCase):
    def test_availability_creation(self):
        availability = AvailabilityFactory.create()
        eq_(availability.pk, 1)

    def test_availability_str(self):
        availability = AvailabilityFactory.create()
        eq_(str(availability), f'{availability.player} - {availability.date}')

    @freeze_time('2018-09-15')
    def test_certain_fill(self):
        availability = AvailabilityFactory.create(
            date=datetime(2018, 9, 15),
            player__team__days_to_fill_ahead_certain=7
        )
        eq_((datetime(2018, 9, 8), False, ), availability.certain_fill())

    @freeze_time('2018-09-15')
    def test_approximate_fill(self):
        availability = AvailabilityFactory.create(
            date=datetime(2018, 9, 15),
            player__team__days_to_fill_ahead_approximate=28
        )
        eq_((datetime(2018, 8, 18), False, ), availability.approximate_fill())
