# Generated by Django 2.1 on 2018-10-02 04:05

import decentmark.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decentmark', '0005_submission_autofeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='autostatus',
            field=models.CharField(choices=[('U', 'UNMARKED'), ('P', 'PENDING'), ('M', 'MARKED'), ('T', 'TIMEDOUT')], default=decentmark.models.SubmissionStatus('U'), max_length=1),
        ),
    ]
