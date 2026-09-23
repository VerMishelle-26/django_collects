from decimal import Decimal
from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Collect, Payment

User = get_user_model()


class CollectTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="pass12345"
        )
        self.collect = Collect.objects.create(
            author=self.user,
            title="Test collect",
            occasion="birthday",
            ends_at=timezone.now() + timedelta(days=30),
            target_amount=Decimal("10000"),
        )

    @patch("collects.views.send_collect_created_email.delay")
    def test_create_collect(self, mock_email):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/collects/", {
            "title": "New collect",
            "occasion": "wedding",
            "ends_at": (timezone.now() + timedelta(days=10)).isoformat(),
            "target_amount": "50000",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Collect.objects.count(), 2)
        mock_email.assert_called_once()

    def test_list_collects(self):
        response = self.client.get("/api/collects/")
        self.assertEqual(response.status_code, 200)

    @patch("collects.views.send_payment_email.delay")
    def test_donate(self, mock_email):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            f"/api/collects/{self.collect.id}/donate/",
            {"amount": "500", "comment": "test"}
        )
        print("\n--- RESPONSE DATA ---")
        print(response.data)     # ← вот это покажет причину
        print("--- END ---")
        self.assertEqual(response.status_code, 201)

    def test_finished_collect(self):
        self.collect.ends_at = timezone.now() - timedelta(days=1)
        self.collect.save()
        self.assertTrue(self.collect.is_finished)