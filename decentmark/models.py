from datetime import datetime as Datetime
from enum import Enum

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_class = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Unit(models.Model):
    name = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()
    deleted = models.BooleanField(default=False)

    def clean(self):
        if self.end and self.start and self.end <= self.start:
            raise ValidationError({
                'end': _('End date should be after start date')
            })

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('decentmark:unit_view', kwargs={'unit_id': self.pk})

class AuditLog(models.Model):
    date = models.DateTimeField(default=Datetime.now, blank=True)
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL, default=None, blank=True, null=True)
    message = models.TextField()

class UnitUsers(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    create = models.BooleanField(default=False)
    mark = models.BooleanField(default=False)
    submit = models.BooleanField(default=True)
    tag = models.CharField(max_length=200, default=None, blank=True, null=True)
    # TEACHER = 'teacher'
    # MARKER = 'marker'
    # STUDENT = 'student'
    # ROLE_CHOICES = (
    #     (TEACHER, 'Teacher'),
    #     (MARKER, 'Marker'),
    #     (STUDENT, 'Student'),
    # )
    # role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return str(self.unit) + " - " + str(self.user)

    class Meta:
        verbose_name = _('Unit User')
        verbose_name_plural = _('Unit Users')


class Assignment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField()
    total = models.IntegerField(default=-1)
    test = models.TextField()
    solution = models.TextField()
    template = models.TextField()
    deleted = models.BooleanField(default=False)

    def clean(self):
        if self.end <= self.start:
            raise ValidationError({
                'end': _('End date should be after start date')
            })
        if self.total < 1:
            raise ValidationError({
                'total': _('Total Mark should be at least 1')
            })

    def __str__(self):
        return str(self.unit) + " - " + str(self.name)

    def get_absolute_url(self):
        return reverse('decentmark:assignment_view', kwargs={'assignment_id': self.pk})

class SubmissionStatus(Enum):
    UNMARKED = 'U'
    PENDING = 'P'
    MARKED = 'M'
    TIMEDOUT = 'T'

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, blank=True)
    solution = models.TextField()
    autostatus = models.CharField(default=SubmissionStatus.UNMARKED.value,
                                  max_length=1,
                                  choices=tuple((status.value, status.name) for status in SubmissionStatus))
    automark = models.IntegerField(default=-1, validators=[MinValueValidator(-1)])
    autofeedback = models.TextField(default="", blank=True)
    mark = models.IntegerField(default=-1, validators=[MinValueValidator(-1)])
    feedback = models.TextField(default="", blank=True)

    def clean(self):
        if self.automark >= 0:
            if self.automark > self.assignment.total:
                raise ValidationError({
                    'mark': _('Mark should be less than or equal to the assignment Total Mark')
                })
        if self.mark >= 0:
            if self.mark > self.assignment.total:
                raise ValidationError({
                    'mark': _('Mark should be less than or equal to the assignment Total Mark')
                })

    def __str__(self):
        return str(self.assignment) + " - " + str(self.user) + " - " + str(self.autostatus)

    def get_absolute_url(self):
        return reverse('decentmark:submission_view', kwargs={'submission_id': self.pk})
