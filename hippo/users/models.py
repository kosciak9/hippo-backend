import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible

from rest_framework.authtoken.models import Token


class Position(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class AdditionalPerk(models.Model):
    name = models.CharField(max_length=200)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Team(models.Model):
    name = models.CharField(max_length=200)
    admin_perk = models.ForeignKey(related_name='AdminPerk',
                                   to=AdditionalPerk,
                                   on_delete=models.SET_NULL,
                                   null=True)
    hour_count = models.IntegerField(default=10)
    hours = models.CharField(max_length=1024)
    days_to_fill_ahead_certain = models.IntegerField(default=7)
    days_to_fill_ahead_approximate = models.IntegerField(default=28)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    kit_number = models.IntegerField(default=99)
    position = models.ForeignKey(Position, null=True,
                                 on_delete=models.SET_NULL)

    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    additional_perks = models.ManyToManyField(AdditionalPerk, blank=True)
    locale = models.CharField(max_length=2, choices=(
        ('en', 'English'),
        ('pl', 'Polski'),
    ), default='pl')

    def __str__(self):
        return self.username

    def __repr__(self):
        return str(self)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Availability(models.Model):
    date = models.DateField()
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.CharField(max_length=1024)
    approximate_available = models.IntegerField()
    edited = models.BooleanField(default=False)

    def certain_fill(self):
        certain_fill_date = self.date - timedelta(
            days=self.player.team.days_to_fill_ahead_certain
        )
        are_you_late = certain_fill_date > datetime.today()
        return certain_fill_date, are_you_late

    def approximate_fill(self):
        approximate_fill_date = self.date - timedelta(
            days=self.player.team.days_to_fill_ahead_approximate
        )
        are_you_late = approximate_fill_date > datetime.today()
        return approximate_fill_date, are_you_late

    def __str__(self):
        return (f'{str(self.player)} - {str(self.date)}')

    def __repr__(self):
        return str(self)
