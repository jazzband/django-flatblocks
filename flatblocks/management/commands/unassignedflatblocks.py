import os

from django.core.management.base import BaseCommand
from django.template.loader import get_template

from django.conf import settings

from flatblocks.templatetags.flatblock_tags import FlatBlockNode
from flatblocks.models import FlatBlock


class Command(BaseCommand):
    help = "List unassigned flatblocks in the templates"

    def handle(self, *args, **options):
        save_nodes = (len(args) and args[0] == 'create')
        flatblock_nodes = set()
        print_nodes = []

        # get list of templates
        for templ_dir in settings.TEMPLATE_DIRS:
            for path, dirlist, fnlist in os.walk(templ_dir):
                for fn in fnlist:
                    try:
                        t = get_template(os.path.join(path, fn))
                        flatblock_nodes.update(
                            flatblock_nodes.update(node.slug for node in t.nodelist.get_nodes_by_type(FlatBlockNode)
                            )
                        )
                    except:
                        # Should log at debug level?
                        pass

        # check if flatblocks have entry in database
        for node in flatblock_nodes:
            if not FlatBlock.objects.filter(slug=node).exists():
                # if create argument was supplied, save empty nodes
                if save_nodes:
                    FlatBlock.objects.create(header="[{0}]".format(node), content="Generated flatblock", slug=node)
                print_nodes.append(node)

        if print_nodes:
            if save_nodes:
                self.stdout.write("Following nodes were created:")
            self.stdout.write("\n".join(print_nodes))
        else:
            self.stdout.write("All FlatBlock items are in database")
