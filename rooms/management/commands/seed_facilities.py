from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):

    # help = "This command creates many users"
    help = "This command creates facilities"

    # def add_arguments(self, parser):
    #     parser.add_argument("--number", help="How many users do you want to create")

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on permises",
            "Paid parking off permises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for a in facilities:
            Facility.objects.create(name=a)
        self.stdout.write(self.style.SUCCESS("Facilities created!"))