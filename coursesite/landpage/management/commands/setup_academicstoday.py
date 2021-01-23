from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from landpage.models import LandpageTeamMember
from landpage.models import LandpagePartner

class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py setup_academicstoday
    """
    help = 'Picks the top 9 courses with the highest student enrollment.'
    
    def handle(self, *args, **options):
        """
            Function will create the objects necessary for some of the UI
            elements in the landpage.
        """
        LandpageTeamMember.objects.all().delete()
        LandpageTeamMember.objects.create(
            id=1,
            full_name="Sidorov Alexander",
            role="Lead Developer",
            twitter_url="https://twitter.com/sanchezgamingtv",
            facebook_url="https://www.facebook.com/alex.thunder.507",
            image_filename="none.png",
            linkedin_url="https://www.linkedin.com/in/alex-sidorov-666351130/",
            email="s1d0r0valexiv@gmail.com",
        )

        LandpagePartner.objects.all().delete()
        # LandpagePartner.objects.create(
        #     id=1,
        #     image_filename="duplexsoft.png",
        #     title="Duplexsoft",
        #     url="www.duplexsoft.com"
        # )
        # LandpagePartner.objects.create(
        #     id=2,
        #     image_filename="eurasiasoft.png",
        #     title="Eurasiasoft",
        #     url="www.eurasiasoft.com"
        # )
