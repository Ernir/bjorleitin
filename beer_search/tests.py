from django.core.urlresolvers import reverse
from django.test import TestCase


class BeerViewsTestCase(TestCase):

    """
    Unit tests for views returning HTML web pages.
    """

    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_table_loader(self):
        response = self.client.get(reverse("index_table"))
        self.assertEqual(response.status_code, 200)

    def test_overview(self):
        response = self.client.get(reverse("overview"))
        self.assertEqual(response.status_code, 200)

    def test_exciting(self):
        response = self.client.get(reverse("exciting"))
        self.assertEqual(response.status_code, 200)

    def test_gift_boxes(self):
        response = self.client.get(reverse("gift_boxes"))
        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        response = self.client.get(reverse("statistics"))
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_api_doc(self):
        response = self.client.get(reverse("api-doc"))
        self.assertEqual(response.status_code, 200)