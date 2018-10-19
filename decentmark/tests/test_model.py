from django.test import TestCase
from decentmark.models import *
from django.contrib.auth import get_user_model
# import datetime
# from django.core.exceptions import ValidationError


class ProfileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_superuser(username='admin', email='admin@decent.mark',
                                                         password='password')
        Profile.objects.create(user=user, create_class='False')

    def test_str(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = str(profile.user)
        self.assertEquals(expected_object_name, str(profile))


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

    def test_url(self):
        response = self.client.get(reverse('decentmark:unit_view', kwargs={'unit_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)


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


class AssignmentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        unit = Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2019-10-25 14:30:59',
                                   description='111', deleted='False')
        Assignment.objects.create(unit=unit, name='Python Lab 1', start='2018-10-28 14:30:59',
                                  end='2018-10-25 14:30:59',
                                  description='111', total=0, test='we', solution='Answer',
                                  template='Template', deleted='False')

    def test_date(self):
        date = Assignment.objects.get(id=1)
        with self.assertRaises(ValidationError):
            date.full_clean()

    def test_total_mark(self):
        unit = Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2019-10-25 14:30:59',
                                   description='111', deleted='False')
        total_mark = Assignment(unit=unit, name='Python Lab 1', start='2018-10-28 14:30:59',
                                end='2019-10-25 14:30:59',
                                description='111', attempts=1, total=-4, test='we', solution='Answer',
                                template='Template', deleted='False')
        with self.assertRaises(ValidationError):
            total_mark.full_clean()

    def test_str(self):
        assignment = Assignment.objects.get(id=1)
        expected_object_name = str(assignment.unit) + " - " + str(assignment.name)
        self.assertEquals(expected_object_name, str(assignment))

    def test_url(self):
        response = self.client.get(reverse('decentmark:assignment_view', kwargs={'assignment_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)


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

    def test_auto_mark(self):
        auto_mark = Submission.objects.get(id=1)
        with self.assertRaises(ValidationError):
            auto_mark.full_clean()

    # def test_mark(self):
    #     user = get_user_model().objects.create_superuser(username='admin', email='admin@decent.mark',
    #                                                      password='password')
    #     unit = Unit.objects.create(name='Python', start='2018-10-25 14:30:59', end='2017-10-25 14:30:59',
    #                                description='111', deleted='False')
    #     assignment = Assignment.objects.create(unit=unit, name='Python Lab 1', start='2018-10-28 14:30:59',
    #                                            end='2019-10-25 14:30:59', description='111', attempts=1, total=10,
    #                                            test='we', solution='Answer', template='Template', deleted='False')
    #     mark = Submission(assignment=assignment, user=user, date='2018-10-28 14:30:59', solution='Answer',
    #                               automark=20, autofeedback='All tests passed',
    #                               mark=20, feedback='Good')
    #     with self.assertRaises(ValidationError):
    #         mark.full_clean()

    def test_str(self):
        submission = Submission.objects.get(id=1)
        expected_object_name = str(submission.assignment) + ' - ' + str(submission.user)
        self.assertEquals(expected_object_name, str(submission))

    def test_url(self):
        a = Submission.objects.get(id=1)
        response = self.client.get(reverse('decentmark:submission_view', kwargs={'submission_id': a.id}), follow=True)
        self.assertEqual(response.status_code, 200)
