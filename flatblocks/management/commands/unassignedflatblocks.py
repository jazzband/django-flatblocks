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
        templ_list = []
        flatblock_nodes = []
        print_nodes = []

        #get list of templates
        for templ_dir in settings.TEMPLATE_DIRS:
            templ_list += [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(templ_dir)) for f in fn]

        #load templates and get FlatBlockNode slugs
        for templ in templ_list:
            try:
                t = get_template(templ)
                flatblock_nodes += [node.slug for node in t.nodelist.get_nodes_by_type(FlatBlockNode)]
            except:
                pass

        #distinct slugs
        flatblock_nodes = list(set(flatblock_nodes))

        #check if flatblocks have entry in database
        for node in flatblock_nodes:
            if FlatBlock.objects.filter(slug=node).count() == 0:
                #if create argument was supplied, save empty nodes
                if save_nodes:
                    block = FlatBlock(header="[{0}]".format(node), content="Generated flatblock", slug=node)
                    block.save()
                print_nodes.append(node)

        if len(print_nodes):
            if save_nodes:
                print "Following nodes were created:"
            print "\n".join(print_nodes)
        else:
            print "All FlatBlock items are in database"