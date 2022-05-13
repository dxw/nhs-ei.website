from abc import ABC
from datetime import datetime

from django.core.management.base import BaseCommand
from faker import Faker
from wagtail.models import Page

from cms.blogs.models import Blog
from cms.pages.models import BasePage
from cms.posts.models import Post
from cms.publications.models import Publication

WORDS = [
    "abdominal",
    "abdominoplasty",
    "abdominocentesis",
    "abdominal aorta",
    "abdominous",
    "abduction",
    "aberrant",
    "abiogenesis",
    "acrocyanosis",
    "acrophobia",
    "acromegaly",
    "active",
    "acute",
    "acute gastritis",
    "acute pyelonephritis",
    "tendon",
    "adduction",
    "adenitis",
    "adenocarcinoma",
    "adenoma",
    "adhesion",
    "afebrile",
    "akinesia",
    "alopecia",
    "amenia",
    "amenorrhea",
    "amniocentesis",
    "amnion",
    "amniotic",
    "amniotic fluid",
    "amniotic sac",
    "analgesia",
    "anastomosis",
    "anemia",
    "anemic",
    "anencephalous",
    "anesthesia",
    "anesthesiologist",
    "anesthesiology",
    "aneurysm",
    "angioplasty",
    "neurofibroma",
    "angiology",
    "Anodonta",
    "anomaly",
    "anopia",
    "anorexia",
    "antepartum",
    "antipyretic",
    "anuresis",
    "anuria",
    "aphasia",
    "aplasia",
    "apnea",
    "apneic",
    "arteriosclerosis",
    "arthritis",
    "arthroplasty",
    "asepsis",
    "asymptomatic",
    "atherosclerotic",
    "atrophy",
    "benign",
    "biopsy",
    "blastoderm",
    "blastoderm",
    "blepharitis",
    "blepharitis",
    "blepharospasm",
    "blepharism",
    "bradycardia",
    "bradycardia",
    "bronchiolitis",
    "bronchitis",
    "bronchopneumonia",
    "bronchoscope",
    "bronchospasm",
    "carcinogenic",
    "carcinoma",
    "cardiac arrest",
    "cardiology",
    "cardiologist",
    "cardiology",
    "cardiomegaly",
    "carditis",
    "cauterization",
    "central",
    "cephalalgia",
    "cephalic",
    "cephalometry",
    "cerebrospinal",
    "cerebrovascular",
    "cerebrum",
    "cheilitis",
    "cheiloschisis",
    "cheilosis",
    "chemotherapy",
    "Cheyne-Stokes respiration",
    "cholecystectomy",
    "cholecystitis",
    "cholecalciferol",
    "abdominous",
    "chondrodystrophy",
    "chronic",
    "chronic pyelonephritis",
    "circumduction",
    "climacteric",
    "colic",
    "colitis",
    "celiocentesis",
    "colonoscope",
    "conception",
    "corneal",
    "coronary thrombosis",
    "craniotomy",
    "craniometer",
    "uranoplasty",
    "cranium",
    "cryptorchidism",
    "cyanosis",
    "cystoparalysis",
    "cystoplegia",
    "cystitis",
    "cytoplast",
    "defibrillation",
    "dehiscence",
    "dental",
    "odontalgia",
    "dermatitis",
    "dermatologist",
    "dermatome",
    "dermatosis",
    "diagnosis",
    "diagnostician",
    "diaphragm",
    "dilation",
    "diplococcus",
    "diplopia",
    "disease",
    "distal",
    "dorsally",
]


class Command(BaseCommand, ABC):
    """
    Usage: poetry run ./manage.py generate_fixtures

    This will create actual pages in the DB so create a fixture set, clear your DB and initialise a new one.

    rm db.sqlite3
    poetry run ./manage.py migrate

    And then dump the content as a set of fixtures:

    poetry run ./manage.pydumpdata \
        -o fixtures/some-fixture-file.json \
        --indent 2 \
        --exclude contenttypes \
        --exclude auth.permission
    """

    help = "Creates fixture data in the DB"

    def __init__(self):
        super().__init__()
        Faker.seed(4321)
        self.faker = Faker()

    def handle(self, *args, **options):
        root = Page.objects.get(title="Home")

        # create some dummy base pages
        for index in range(10):
            page = BasePage()
            self.populate(page)
            root.add_child(instance=page)
            page.save()

        # create some dummy Post pages
        for index in range(10):
            page = Post()
            self.populate(page)
            root.add_child(instance=page)
            page.save()

        # create some dummy Blog pages
        for index in range(10):
            page = Blog()
            self.populate(page)
            root.add_child(instance=page)
            page.save()

        # create some dummy Publication pages
        for index in range(10):
            page = Publication()
            self.populate(page)
            root.add_child(instance=page)
            page.save()

        # create some dummy Page pages
        for index in range(10):
            page = Page()
            self.populate(page)
            root.add_child(instance=page)
            page.save()

    def populate(self, obj):
        title_array = self.faker.sentence(ext_word_list=WORDS).split()[0:3]
        obj.title = " ".join(title_array)
        obj.latest_revision_created_at = self.faker.date_time_between(
            start_date=datetime(2019, 1, 1), end_date=datetime(2021, 12, 31)
        )
        return obj
