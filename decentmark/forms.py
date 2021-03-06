from django import forms
from django.forms import ModelForm, DateInput, Form
from decentmark.models import Unit, Assignment, Submission


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


class UnitUsersForm(Form):
    users = forms.FileField()
    create = forms.BooleanField(required=False)
    mark = forms.BooleanField(required=False)
    submit = forms.BooleanField(required=False)


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = (
            'name',
            'start',
            'end',
            'description',
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
            'automark',
            'mark',
            'autofeedback',
            'feedback',
        )

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['solution'].disabled = True
        self.fields['automark'].disabled = True
        self.fields['autofeedback'].disabled = True


