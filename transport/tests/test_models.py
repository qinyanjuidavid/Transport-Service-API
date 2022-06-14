from locale import currency
from django.test import TestCase
import datetime

from rest_framework.test import APITestCase
from transport.models import Provider, ServiceArea


class TestProviderModel(APITestCase):
    def setUp(self, **kwargs):
        self.provider = Provider.objects.create(
            name="testuser",
            email="testmail@mozio.com",
            phone="+254700215648",
            language="Swahili",
            currency="USD"
        )
        self.provider.save()

    def test_provider(self):
        self.assertIsInstance(self.provider, Provider)
        self.assertEqual(self.provider.name, "testuser")
        self.assertEqual(self.provider.email, "testmail@mozio.com")
        self.assertEqual(self.provider.phone, "+254700215648")
        self.assertEqual(self.provider.language, "Swahili")
        self.assertEqual(self.provider.currency, "USD")
        self.assertEqual(self.provider.__str__(), self.provider.name)


class TestServiceAreaModel(APITestCase):
    def setUp(self, **kwargs):
        self.area = ServiceArea.objects.create(
            provider=Provider.objects.create(
                name="testuser",
                email="testmail@mozio.com",
                phone="+254700215648",
                language="Swahili",
                currency="USD"
            ),
            name="free area",
            price=100.0,
            geom=""
        )

    def test_serviceArea(self):

        self.assertIsInstance(self.area, ServiceArea)
        self.assertEqual(self.area.name, "free area")
        self.assertEqual(self.area.price, 100.0)
        self.assertEqual(self.area.__str__(), self.area.name)
        self.assertEqual(self.area.provider.name, "testuser")
        self.assertEqual(self.area.provider.email,
                         "testmail@mozio.com")
        self.assertEqual(self.area.provider.phone, "+254700215648")
        self.assertEqual(self.area.provider.language, "Swahili")
        self.assertEqual(self. area.provider.currency, "USD")
        self.assertEqual(self.area.provider.__str__(),
                         self.area.provider.name)
