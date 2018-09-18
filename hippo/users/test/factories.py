from random import randint

import factory
from faker import Faker
from hippo.users.models import (AdditionalPerk, Availability, Position, Team,
                                User)

fake = Faker()


class PositionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Position

    name = factory.Faker('name')


class AdditionalPerkFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AdditionalPerk

    name = factory.Faker('sentence')
    visible = factory.Faker('pybool')


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    id = factory.Faker('uuid4')
    username = factory.Sequence(lambda n: f'testuser{n}')
    password = factory.Faker('password', length=10, special_chars=True,
                             digits=True, upper_case=True, lower_case=True)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    position = factory.SubFactory(PositionFactory)
    kit_number = factory.Faker('pyint')
    team = factory.SubFactory('hippo.users.test.factories.TeamFactory')

    @factory.post_generation
    def additional_perks(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for perk in extracted:
                self.additional_perks.add(perk)


def generate_random_hours_string():
    count = randint(1, 30)
    hours_list = []
    for _ in range(count):
        hours_list.append(fake.time(pattern='%H:%M'))
    hours_list.sort()
    hours = ','.join(hours_list)
    return hours


class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Team

    name = factory.Faker('company')
    admin_perk = factory.SubFactory(AdditionalPerkFactory)
    hour_count = factory.Faker('pyint')
    hours = generate_random_hours_string()
    days_to_fill_ahead_certain = factory.Faker('pyint')
    days_to_fill_ahead_approximate = factory.Faker('pyint')


def generate_random_availability():
    count = randint(1, 30)
    availability_list = []
    for _ in range(count):
        availability_list.append(str(fake.pybool()))
    available = ','.join(availability_list)
    return available


class AvailabilityFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Availability

    date = factory.Faker('date')
    player = factory.SubFactory(UserFactory)
    available = generate_random_availability()
    approximate_available = factory.Faker('pyint')
    edited = factory.Faker('pybool')
