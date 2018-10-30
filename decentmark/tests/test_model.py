from django.test import TestCase
from decentmark.models import *
from django.contrib.auth import get_user_model
# import datetime
# from django.core.exceptions import ValidationError


class UnitModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2017-10-25 14:30:59', description='111',
                            deleted='False')

    def test_name_label(self):
        unit = Unit.objects.get(id=1)  # type: Unit
        field_label = unit._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        unit = Unit.objects.get(id=1)
        max_length = unit._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_str(self):
        unit = Unit.objects.get(id=1)
        expected_object_name = unit.name
        self.assertEquals(expected_object_name, str(unit))

    def test_date(self):
        unit = Unit.objects.get(id=1)
        with self.assertRaises(ValidationError):
            unit.full_clean()


class UnitUsersTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        unit = Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2017-10-25 14:30:59',
                                   description='111', deleted='False')
        user = get_user_model().objects.create_superuser(username='admin', email='admin@decent.mark',
                                                         password='password')
        UnitUsers.objects.create(unit=unit, user=user, create='False', mark='False', submit='True')

    def test_str(self):
        unit_user = UnitUsers.objects.get(id=1)
        expected_object_name = str(unit_user.unit) + ' - ' + str(unit_user.user)
        self.assertEquals(expected_object_name, str(unit_user))

    # def test_verbose_name(self):
    #     unit_user = Unit.objects.get(id=1)
    #     field_label = unit_user._meta.get_field('Unit User').verbose_name
    #     self.assertEquals(field_label, 'Unit User')
    #
    # def test_verbose_name_plural(self):
    #     unit_user = Unit.objects.get(id=1)
    #     field_label = unit_user._meta.get_field('Unit Users').verbose_name_plural
    #     self.assertEquals(field_label, 'Unit Users')


class AssignmentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        unit = Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2017-10-25 14:30:59',
                                   description='111', deleted='False')
        Assignment.objects.create(unit=unit, name='Python Lab 1', start='2018-10-28 14:30:59',
                                  end='2018-10-25 14:30:59',
                                  description='111', total=0, test='we', solution='Answer',
                                  template='Template', deleted='False')

    def test_date(self):
        date = Assignment(start='2018-10-28 14:30:59', end='2018-10-25 14:30:59')
        with self.assertRaises(ValidationError):
            date.full_clean()

    def test_total_mark(self):
        t = Assignment(total=0)
        with self.assertRaises(ValidationError):
            t.full_clean()

    def test_str(self):
        assignment = Assignment.objects.get(id=1)
        expected_object_name = str(assignment.unit) + " - " + str(assignment.name)
        self.assertEquals(expected_object_name, str(assignment))


class SubmissionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_superuser(username='admin', email='admin@decent.mark',
                                                         password='password')
        unit = Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2017-10-25 14:30:59',
                                   description='111', deleted='False')
        assignment = Assignment.objects.create(unit=unit, name='Python Lab 1', start='2018-10-28 14:30:59',
                                               end='2018-10-25 14:30:59', description='111', total=0,
                                               test='we', solution='Answer', template='Template', deleted='False')
        Submission.objects.create(assignment=assignment, user=user, date='2018-10-28 14:30:59', solution='Answer',
                                  automark=10, autofeedback='All tests passed',
                                  mark=10, feedback='Good')

    def test_mark(self):
        mark = Submission(mark=0)
        with self.assertRaises(ValidationError):
            mark.full_clean()

    def test_str(self):
        submission = Submission.objects.get(id=1)
        expected_object_name = str(submission.assignment) + ' - ' + str(submission.user)
        self.assertEquals(expected_object_name, str(submission))
