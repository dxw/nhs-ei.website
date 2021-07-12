import logging

from django.core.management.base import BaseCommand
from cms.publications.models import PublicationPublicationTypeRelationship
from cms.categories.models import PublicationType

logger = logging.getLogger(__name__)

USELESS_PUBLICATIONS = [
    "briefings",
    "invitations",
    "lean",
    "nhs volunteer responders referal",
    "statistics",
    "collaborations",
    "improvement",
    "refer to nhs volunteers",
]

PUBLICATION_MERGERS = {
    "Newsletter": "Newsletter or bulletin",
    "Policy": "Policy and strategy",
    "Policy or strategy": "Policy and strategy",
}


def deduplicate_publicationtypes():
    """Replace the publication type IDs associated with each publication with the ID
    of the publication type we're keeping."""
    accepted_mappings = {}
    pubtypes = PublicationType.objects.all()
    count = 0
    for pubtype in pubtypes:
        # use proper name if merging different strings and save in case changed
        name = pubtype.name
        if name in USELESS_PUBLICATIONS:
            replace_publication_type(pubtype.id, None)
            count += 1
        name = PUBLICATION_MERGERS.get(name, name)
        pubtype.save()
        # use lowercase for string matching - either accept as the new mapping
        # or change it to the pre-accepted one
        lname = name.lower()
        if lname in accepted_mappings:
            replace_publication_type(pubtype.id, accepted_mappings[lname])
            count += 1
        else:
            accepted_mappings[lname] = pubtype.id


def replace_publication_type(old, new):
    relationships = PublicationPublicationTypeRelationship.objects.filter(
        publication_type_id=old
    )
    if new is None:
        assert not relationships, len(relationships)
    print(f"{len(relationships)} move from {old} to {new}")

    for relation in relationships:
        relation.publication_type_id = new
        relation.save()
        relation.validate_unique()

    pubtype = PublicationType.objects.get(id=old)
    print(f"deleting {old} {pubtype.name}")
    pubtype.delete()


class Command(BaseCommand):
    """
    Each sub_site had a different set of 'publication types', but we want to unify these.
    """

    help = "Deduplicate publication types"

    def handle(self, *args, **options):
        deduplicate_publicationtypes()
