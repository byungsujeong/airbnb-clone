import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists.models import List
from users.models import User
from rooms.models import Room


class Command(BaseCommand):

    help = "This command creates many lists"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many lists you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(
            List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        for pk in created_clean:
            list_model = List.objects.get(pk=pk)
            for r in rooms:
                magic_number = random.randint(0, 12)
                if magic_number % 12 == 0:
                    list_model.rooms.add(r)
        self.stdout.write(self.style.SUCCESS(f"{number} lists created!"))