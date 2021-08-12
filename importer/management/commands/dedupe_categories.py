import logging

from django.core.management.base import BaseCommand
from cms.categories.models import CategoryPageCategoryRelationship, Category
from cms.publications.models import PublicationType

logger = logging.getLogger(__name__)

DELETE = []
# from: to
MERGE = {
    "Allied health professionals bulletin": "Allied Health Professionals",
    "Business plan 2012-2015: indicators and other key data": "Business plan",
    "CCG learning network news": "CCG learning and support tool",
    "Commissioning Support Bulletin": "Commissioning",
    "Diabetes": "Diabetes and Kidney Care",
    "Diagnostics waiting times and activity data": "Diagnostics",
    "Diagnostic imaging dataset": "Diagnostics",
    "Efficiencies": "Efficiency and Waste Reduction",
    "Liason and Diversion Bulletin": "Liason and diversion",
    "Mental Health Community Teams Activity": "Mental Health",
    "News and updates": "News",
    "Specialised Commissioning Stakeholder Bulletin": "Specialised commissioning",
    "Statistics Information": "Statistics",
    "Sustainability": "Sustainability and transformation partnerships",
    "System Transformation": "Sustainability and transformation partnerships",
    "Winter news, advice and blogs": "Winter news and advice",
    "statistics data downloads": "Statistics",
}


def deduplicate_categories():
    categories = Category.objects.all()
    accepted_mappings = {}
    for cat in categories:
        original = cat.name
        collision = MERGE.get(original, original).lower()
        if collision in accepted_mappings:
            replace_category(cat.id, accepted_mappings[collision])
        else:
            print(
                f"Keeping {Category.objects.filter(id=cat.id)} records in {cat.id} {cat.name}"
            )
            accepted_mappings[collision] = cat.id


def replace_category(old, new):
    # Move objects in the old category to the new one.
    # New can be None if the category is empty.
    relationships = CategoryPageCategoryRelationship.objects.filter(category_id=old)
    if new is None:
        assert not relationships, len(relationships)
    print(f"{len(relationships)} move from {old} to {new}")

    for relation in relationships:
        relation.category_id = new
        relation.save()
        relation.validate_unique()

    cat = Category.objects.get(id=old)
    assert not CategoryPageCategoryRelationship.objects.filter(category_id=old)
    print(f"deleting empty category {old}: {cat.name}")
    cat.delete()


class Command(BaseCommand):
    """
    Each sub_site had a different set of categories, but we want to unify these.
    """

    help = "Deduplicate categories"

    def handle(self, *args, **options):
        deduplicate_categories()
