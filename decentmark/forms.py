import random
import string
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from decentmark.models import Unit, Assignment, Submission, UnitUsers


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = (
            'name',
            'start',
            'end',
            'description',
        )
        widgets = {
            'start': DateInput(attrs={'type': 'date'}),
            'end': DateInput(attrs={'type': 'date'}),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
        )

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
        user = User.objects.create_user(email, email=email, password=password)

        # send email
        subject = 'account creation'
        message = 'username: %s\npassword %s' % (user.get_username(), password)
        user.email_user(subject, message, fail_silently=False)

        return user


class UnitUsersForm(ModelForm):
    class Meta:
        model = UnitUsers
        fields = (
            'user',
        )


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = (
            'name',
            'start',
            'end',
            'description',
            'attempts',
            'total',
            'test',
            'solution',
            'template',
        )
        widgets = {
            'start': DateInput(attrs={'type': 'date'}),
            'end': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)


class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = (
            'solution',
        )


class FeedbackForm(ModelForm):
    class Meta:
        model = Submission
        fields = (
            'solution',
            'mark',
            'feedback',
        )

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['solution'].disabled = True
