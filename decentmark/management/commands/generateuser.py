# how to run file > python manage.py generateuser -un 2
# 2 -  number of users to be created
import random
import sys
from django.core.management.base import BaseCommand, CommandError, CommandParser
from decentmark.models import Unit
from datetime import date,timedelta
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Generate/regenerate unit with random content'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-un', '--user-number', type=str, required=True,
                            help="Number of the generated users",dest="un")


    def handle(self, *args, **options):
        # print(date.today())
        # Generate a random seed (Source: https://stackoverflow.com/a/5012617)
        if(options['un'] == None):
            print("Please specify number of units to be added")
        else:
            un = int(options['un'])
            for x in range(0,un):
                user=User.objects.create_user(
                    'user- '+str(x), 
                    password='password'
                    )
                user.save()
                print(str(user)+ " created.")
