# how to run file > python manage.py generatedata -un 2 -an 4 -sn 6
# 2- number of units
# 4 - number of assignments in each unit
# 6 - number of submission in each assignment

import random
import sys
from django.core.management.base import BaseCommand, CommandError, CommandParser
from decentmark.models import Unit,Assignment,Submission,UnitUsers
from datetime import date,timedelta
from django.contrib.auth.models import User
from django.utils import timezone
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


users = User.objects.all()

class Command(BaseCommand):
    help = 'Generate/regenerate unit with random content'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-un', '--unit-number', type=int, required=True,
                            help="Number of units generated",dest="un")
        parser.add_argument('-an', '--assignment-number', type=int, required=True,
                            help="Number of assignment generated",dest="an")
        parser.add_argument('-sn', '--submission-number', type=int, required=True,
                            help="Number of submission generated",dest="sn")

    def handle(self, *args, **options):
        # print(date.today())
        # Generate a random seed (Source: https://stackoverflow.com/a/5012617)
        un = int(options['un'])
        an = int(options['an'])
        sn = int(options['sn'])
        #create units
        assignment_end = date.today()
        unit_end = date.today()
        random.seed(4)
        for x in range(0,un): 
            unit_start = unit_end + timedelta(days=int(10*(random.random())));
            unit_end = unit_start + timedelta(days=30);
            random.seed()
            unit = Unit.objects.create(
                name = "Unit "+ str(x+1),
                description="Description about the Unit",
                start = unit_start,
                end = unit_end + timedelta(days=30),
                deleted = 0
                )
            unit.save()
            print("Unit with name "+str(unit.name)+ " created.")
            usernumber = 0
            #make a user teacher
            unituser = UnitUsers.objects.create(
                unit = unit,
                user = users[usernumber],
                create = True,
                mark = False,
                submit = False
                )
            unituser.save()
            random.seed(3)
            #create assignments with user teacher
            for y in range(0,an):
                assignment_start = assignment_end +timedelta(days=int(10*(random.random())))
                assignment_end = assignment_start +timedelta(days=int(10*(random.random())+5))
                assignment = Assignment.objects.create(
                    unit = unit,
                    name = "Assignment" + str(y+1),
                    start = assignment_start,
                    end = assignment_end,
                    description="Description about the Assignment",
                    attempts = random.randint(1,21),
                    total = 100,
                    test = "random test here! ",
                    solution =  "random solution here! ",
                    template =  "random template here! ",
                    deleted = False
                    )
                assignment.save()
                print("Assignment with name "+str(assignment.name)+ " created.")
                usernumber = usernumber+1
            #assign 2 marker users for the unit
            for x in range(0,2):
                unituser = UnitUsers.objects.create(
                    unit = unit,
                    user = users[usernumber],
                    create = False,
                    mark = True,
                    submit = False
                    )
                unituser.save()
                usernumber = usernumber+1
            random.seed(3)
            assignment_start = date.today() +timedelta(days=int(10*(random.random())))
            #assign 10 student users for the unit
            for x in range(0,sn):
                submission_date = assignment_start +timedelta(days=int(10*(random.random())))
                unituser = UnitUsers.objects.create(
                    unit = unit,
                    user = users[usernumber],
                    create = False,
                    mark = False,
                    submit = True
                    )
                unituser.save()
                submission = Submission.objects.create(
                    user = users[usernumber],
                    assignment = assignment,
                    date = submission_date,
                    marked = True,
                    mark = random.randrange(0, 100),
                    feedback = "some feedback here"
                    )
                submission.save()
                print("Submission with name "+str(submission)+ " created.")
                usernumber = usernumber+1
