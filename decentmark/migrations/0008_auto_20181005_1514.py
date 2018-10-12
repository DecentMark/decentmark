# Generated by Django 2.1.2 on 2018-10-05 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decentmark', '0007_remove_assignment_attempts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='autostatus',
            field=models.CharField(choices=[('U', 'UNMARKED'), ('P', 'PENDING'), ('M', 'MARKED'), ('T', 'TIMEDOUT')], default='U', max_length=1),
        ),
    ]