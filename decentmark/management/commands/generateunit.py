import random
import sys
from django.core.management.base import BaseCommand, CommandError, CommandParser
from decentmark.models import Unit

class Command(BaseCommand):
    help = 'Generate/regenerate unit with random content'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('-un', '--unit-name', type=str, required=False,
                            help="Name of the generated unit")
        parser.add_argument('-s', '--seed', type=int, required=False,
                            help="Random number generator seed")

    def handle(self, *args, **options):
        # Generate a random seed (Source: https://stackoverflow.com/a/5012617)
        if options['seed'] is None:
            seed = random.randrange(sys.maxsize)
        else:
            seed = options['seed']
        self.stdout.write("Random Seed: %d" % seed)

        rand = random.Random()
        rand.seed(seed, version=2)

        if options['unit_name'] is None:
            unit_name = 'TEST' + "".join(map(str, rand.choices(range(10), k=4)))
        else:
            unit_name = options['unit_name']
        self.stdout.write("Unit Name: " + unit_name)
