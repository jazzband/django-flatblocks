from django.core.management import BaseCommand, CommandError
from django.db import IntegrityError

from flatblocks.models import FlatBlock


class Command(BaseCommand):
    help = "Create a new flatblock with the given slug"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError, "This command requires the slug of the new " \
                                "flatblock as its first argument"
        slug = args[0]
        block = FlatBlock(header="[%s]"%slug, content="Empty flatblock",
                slug=slug)
        try:
            block.save()
        except IntegrityError, e:
            raise CommandError, "A flatblock with this name already exists"
