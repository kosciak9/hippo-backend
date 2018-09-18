from django.forms.models import model_to_dict
from django.urls import reverse
from nose.tools import eq_

from faker import Faker
from hippo.users.models import Position
from hippo.users.test.factories import PositionFactory, UserFactory
from rest_framework import status
from rest_framework.test import APITestCase

fake = Faker()


class TestPositionListTestCase(APITestCase):
    """
    Tests /positions list operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.position_data = model_to_dict(PositionFactory.build())
        self.url = reverse('position-list')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}'
        )

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.position_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        position = Position.objects.get(pk=response.data.get('pk'))
        eq_(position.name, self.position_data.get('name'))


class TestPositionDetailTestCase(APITestCase):
    """
    Tests /position detail operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.position = PositionFactory()
        self.url = reverse('position-detail', kwargs={'pk': self.position.pk})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}'
        )

    def test_get_request_returns_a_given_position(self):
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_put_request_cant_update_a_position(self):
        new_position_name = fake.name()
        payload = {'name': new_position_name}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_position(self):
        self.user.team_admin = True
        self.user.save()
        new_position_name = fake.name()
        payload = {'name': new_position_name}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)


class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('user-list')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.user.auth_token}'
        )

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
