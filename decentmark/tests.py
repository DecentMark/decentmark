from django.test import TestCase

from decentmark.models import Unit
import datetime
from django.core.exceptions import ValidationError



class UnitModelTest(TestCase):
    def setUpTestData(cls):
        Unit.objects.create(name='Python')

    def test_name_label(self):
        unit = Unit.objects.get()  # type: Unit
        field_label = unit._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        unit = Unit.objects.get()
        max_length = unit._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

