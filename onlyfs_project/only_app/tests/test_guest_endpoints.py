import pytest
from rest_framework.test import APITestCase
from django.shortcuts import reverse
from conftest import EVERYTHING_EQUALS_NOT_NONE


pytestmark = [pytest.mark.django_db]


class TestCategoriesVies(APITestCase):
    fixtures = ['only_app/tests/fixtures/categories_fixture.json']
    def test_categories_list_endpoints(self):
        url = reverse('categories')
        responce = self.client.get(url)
        assert responce.status_code == 200
        assert isinstance(responce.data, list)
        assert responce.data == [
            {
                "id": 1,
                "name": EVERYTHING_EQUALS_NOT_NONE,
                "description": EVERYTHING_EQUALS_NOT_NONE
            },

        ]


