from django.test import TestCase


# Create your tests here.
class S3TestCase(TestCase):

    def test_s3_example1(self):
        self.assertEqual(1 + 1, 2)
