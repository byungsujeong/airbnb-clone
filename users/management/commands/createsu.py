from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command createe superuser"

    def handle(self, *args, **options):

        admin = User.objects.get_or_none(username="admin")
        if not admin:
            User.objects.create_superuser(
                "admin", "byungsu.jeong88@gmail.com", "1q2w3e4r!@"
            )
            self.stdout.write(self.style.SUCCESS("Superusers Created!"))
        else:
            self.stdout.write(self.style.SUCCESS("Superusers Exist!"))