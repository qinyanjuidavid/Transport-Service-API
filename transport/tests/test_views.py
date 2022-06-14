import json
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from transport.models import Provider, ServiceArea
import pdb
from django.contrib.gis.geos import Polygon, MultiPolygon
from rest_framework.reverse import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.test.client import RequestFactory
from django.test import Client


class TestSetUp(APITestCase):
    def setUp(self):
        # Create polygons and pass them as a list in the multipolygon
        self.p1 = Polygon(((0.0, 0.0), (0.0, 50.0),
                           (50.0, 50.0), (50.0, 0.0),
                           (0.0, 0.0)))
        self.p2 = Polygon(((0.0, 0.0), (0.0, 33.0),
                           (33.0, 33.0), (33.0, 0.0),
                           (0.0, 0.0)))
        self.data = {
            "name": "testuser",
            "email": "testmail@mozio.com",
            "phone": "+254700215645",
            "language": "Swahili",
            "currency": "USD",
            "areaName": "free Area",
            "price": 350,
            "geom": MultiPolygon([self.p1, self.p2])


        }
        return super().setUp()

    # Ensure the db rolls back to it's initial state
    def tearDown(self) -> None:
        return super().tearDown()


class test_provider_view(TestSetUp):
    def test_provider_list(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        res = self.client.get(api_reverse("api:provider-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], provider.name)
        self.assertEqual(res.data[0]["email"], provider.email)
        self.assertEqual(res.data[0]["phone"], provider.phone)
        self.assertEqual(res.data[0]["language"], provider.language)
        self.assertEqual(res.data[0]["currency"], provider.currency)

    def test_can_get_provider_detail(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        res = self.client.get(api_reverse(
            "api:provider-detail", kwargs={"pk": provider.pk}))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["name"], provider.name)
        self.assertEqual(res.data["email"], provider.email)
        self.assertEqual(res.data["phone"], provider.phone)
        self.assertEqual(res.data["language"], provider.language)
        self.assertEqual(res.data["currency"], provider.currency)

    def test_can_create_provider(self):
        payload = {
            "name": self.data["name"],
            "email": self.data["email"],
            "phone": self.data["phone"],
            "language": self.data["language"],
            "currency": self.data["currency"]
        }
        # pdb.set_trace()
        res = self.client.post(api_reverse("api:provider-list"), payload,
                               format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Provider.objects.count(), 1)
        self.assertEqual(Provider.objects.get().name, self.data["name"])
        self.assertEqual(Provider.objects.get().email, self.data["email"])
        self.assertEqual(Provider.objects.get().phone, self.data["phone"])
        self.assertEqual(Provider.objects.get().language,
                         self.data["language"])
        self.assertEqual(Provider.objects.get().currency,
                         self.data["currency"])

    def test_can_update_provider(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        payload = {
            "name": "John Doe",
            "email": "doe@mozio.com"
        }
        res = self.client.get(api_reverse(
            "api:provider-detail", kwargs={"pk": provider.pk}),
            payload, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Provider.objects.count(), 1)
        self.assertNotEqual(Provider.objects.get().name, payload["name"])
        self.assertNotEqual(Provider.objects.get().email, payload["email"])
        self.assertEqual(Provider.objects.get().phone, provider.phone)
        self.assertEqual(Provider.objects.get().language, provider.language)
        self.assertEqual(Provider.objects.get().currency, provider.currency)

    def test_can_delete_provider(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        res = self.client.delete(api_reverse(
            "api:provider-detail", kwargs={"pk": provider.pk}))
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Provider.objects.count(), 0)


class test_service_area_view(TestSetUp):

    def test_service_area_list(self):
        service_area = ServiceArea.objects.create(
            provider=Provider.objects.create(
                name=self.data["name"],
                email=self.data["email"],
                phone=self.data["phone"],
                language=self.data["language"],
                currency=self.data["currency"]
            ),
            name=self.data["areaName"],
            price=self.data["price"],
            geom=self.data["geom"]
        )

        res = self.client.get(api_reverse("api:servicearea-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(ServiceArea.objects.count(), 1)

    def test_can_get_service_area_detail(self):
        service_area = ServiceArea.objects.create(
            provider=Provider.objects.create(
                name=self.data["name"],
                email=self.data["email"],
                phone=self.data["phone"],
                language=self.data["language"],
                currency=self.data["currency"]
            ),
            name=self.data["areaName"],
            price=self.data["price"],
            geom=self.data["geom"]
        )
        res = self.client.get(api_reverse(
            "api:servicearea-detail", kwargs={"pk": service_area.pk}))
        self.assertEqual(res.status_code, 200)

    def test_can_create_service_area(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        payload = {
            "provider": provider.pk,
            "name": self.data["areaName"],
            "price": self.data["price"],
            "geom": "MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))",
        }
        res = self.client.post(api_reverse(
            "api:servicearea-list"), payload,
            format="json")
        print(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(ServiceArea.objects.count(), 1)

    def test_can_update_service_area(self):
        service_area = ServiceArea.objects.create(
            provider=Provider.objects.create(
                name=self.data["name"],
                email=self.data["email"],
                phone=self.data["phone"],
                language=self.data["language"],
                currency=self.data["currency"]
            ),
            name=self.data["areaName"],
            price=self.data["price"],
            geom=self.data["geom"]
        )
        payload = {
            "name": "John Doe",
            "price": "100"
        }
        res = self.client.get(api_reverse(
            "api:servicearea-detail", kwargs={"pk": service_area.pk}),
            payload, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(ServiceArea.objects.count(), 1)
        self.assertNotEqual(ServiceArea.objects.get().name, payload["name"])
        self.assertNotEqual(ServiceArea.objects.get().price, payload["price"])

    def test_can_delete_service_area(self):
        service_area = ServiceArea.objects.create(
            provider=Provider.objects.create(
                name=self.data["name"],
                email=self.data["email"],
                phone=self.data["phone"],
                language=self.data["language"],
                currency=self.data["currency"]
            ),
            name=self.data["areaName"],
            price=self.data["price"],
            geom=self.data["geom"]
        )
        res = self.client.delete(api_reverse(
            "api:servicearea-detail", kwargs={"pk": service_area.pk}))
        self.assertEqual(res.status_code, 204)
        self.assertEqual(ServiceArea.objects.count(), 0)

    def test_can_get_service_area_list_by_provider(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        service_area = ServiceArea.objects.create(
            provider=provider,
            name=self.data["areaName"],
            price=self.data["price"],
            geom=self.data["geom"]
        )

        res = self.client.get(
            "/api/v1/servicearea/filterServiceArea/?lat=1&lng=1")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(ServiceArea.objects.count(), 1)

    def test_empty_service_area_list(self):
        provider = Provider.objects.create(
            name=self.data["name"],
            email=self.data["email"],
            phone=self.data["phone"],
            language=self.data["language"],
            currency=self.data["currency"]
        )
        service_area = ServiceArea.objects.create(
            provider=provider,
            name=self.data["areaName"],
            price=self.data["price"],
            geom=self.data["geom"]
        )
        res = self.client.get(
            "/api/v1/servicearea/filterServiceArea/")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["message"],
                         "Please provide latitude and longitude")
