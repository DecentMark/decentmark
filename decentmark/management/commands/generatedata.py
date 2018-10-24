# how to run file > python manage.py generatedata -un 2 -an 4 -s 6 -y 2018
# 2- number of units
# 4 - number of assignments in each unit
# 6 - seed
# 2018 -year

import random
import sys
from django.core.management.base import BaseCommand, CommandError, CommandParser
from decentmark.models import Unit,Assignment,Submission,UnitUsers
from datetime import date,timedelta
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


users = User.objects.all()
feedback = ['Wrong', 'Partially correct', 'Incomplete', 'Complete', 'Correct', "Excellent"]

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

class Command(BaseCommand):
    help = 'Generate/regenerate unit with random content'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-un', '--unit-number', type=str, required=True,
                            help="Number of units generated",dest="un")
        parser.add_argument('-an', '--assignment-number', type=str, required=True,
                            help="Number of assignment generated",dest="an")
        parser.add_argument('-s', '--seed', type=str, required=True,
                            help="seed for random data",dest="seed")
        parser.add_argument('-y', '--year', type=int, required=True,
                            help="Number of submission generated",dest="year")

    def handle(self, *args, **options):
        # print(date.today())
        # Generate a random seed (Source: https://stackoverflow.com/a/5012617)
        un = int(options['un'])
        an = int(options['an'])
        seed = int(options['seed'])
        year = int(options['year'])
        #create units
        d = datetime.date(year, 1, 1)
        unit_start = next_weekday(d, 0)
        unit_end = unit_start + timedelta(days=30)
        unit_end = next_weekday(unit_end, 4)
        random.seed(seed)
        print("seed is "+str(seed))
        for x in range(0,un): 
            unit_end = unit_start + timedelta(days=30)
            unit_end = next_weekday(unit_end, 4)
            random.seed(seed)
            unit = Unit.objects.create(
                name = "Unit "+ str(x+1),
                description="Description about the Unit",
                start = unit_start,
                end = unit_end + timedelta(days=30),
                deleted = 0
                )
            unit.save()
            print("Unit:"+str(unit.name))
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
            random.seed(seed)
            #create assignments with user teacher
            assignment_start = unit_start
            assignment_end = next_weekday(unit_start,4)
            for y in range(0,an):
                assignment = Assignment.objects.create(
                    unit = unit,
                    name = "Assignment" + str(y+1),
                    start = assignment_start,
                    end = assignment_end,
                    description="Description about the Assignment",
                    total = 100,
                    test = "random test here! ",
                    solution =  "random solution here! ",
                    template =  "random template here! ",
                    deleted = False
                    )
                assignment.save()
                print("Assignment:"+str(assignment.name))
                assignment_start = next_weekday(assignment_start,0)
                assignment_end = next_weekday(assignment_start,4)
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
                temp_user = usernumber
                print("User:"+str(users[usernumber])+"created to mark this unit")
            random.seed(seed)
            assignment_start = date.today() +timedelta(days=int(10*(random.random())))
            #assign 10 student users for the unit
            for x in range(0,9):
                unituser = UnitUsers.objects.create(
                    unit = unit,
                    user = users[usernumber],
                    create = False,
                    mark = False,
                    submit = True
                    )
                unituser.save()
                assignmentcount = Assignment.objects.all().filter(unit=unit).count()
                assignments = Assignment.objects.all().filter(unit=unit)
                for xy in range (0,assignmentcount):
                    sn = random.randint(0,5)
                    submission_date = assignments[xy].start +timedelta(days=random.randint(0,5))
                    for x in range(0,sn):
                        submission = Submission.objects.create(
                            user = users[usernumber],
                            assignment = assignments[xy],
                            date = submission_date,
                            mark = random.randrange(0, 100),
                            feedback = random.choice(feedback)
                            )
                        #some random strings
                        submission.save()
                        print("Submission: "+str(submission)+ "Assignment"+str(assignments[xy])+ "User:"+str(users[usernumber])+ "Submission Number"+str(sn))
                usernumber = usernumber+1
            unit_start = unit_end
            unit_start = next_weekday(unit_start, 0)
