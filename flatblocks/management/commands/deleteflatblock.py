from django.core.management import BaseCommand, CommandError

from flatblocks.models import FlatBlock


class Command(BaseCommand):
    help = "Delete a flatblock with the given slug"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError, "This command requires the slug of the " \
                                "flatblock as its first argument"
        slug = args[0]
        try:
            FlatBlock.objects.get(slug=slug).delete()
        except FlatBlock.DoesNotExist, e:
            raise CommandError, "The requested flatblock doesn't exist"

