from django.core.management.base import BaseCommand
from smashers.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
import smptlib

class Command(BaseCommand):
    help = 'Loads the seniors from the json returned by the scraper'

    def handle(self, *args, **options):
        for up in UserProfile.objects.all():
            if up.user is not None:
                self._email_matches(up)

    def _email_matches(self, user_profile):
        matches = user_profile.people_i_like.all() & user_profile.people_like_me.all()
        matches = matches.order_by('name')
        num_matches = matches.count()
        if num_matches < 1:
            return
        if num_matches == 1:
            title = 'You have 1 match on JumboSmash!'
        else:
            title = 'You have {} matches on JumboSmash!'.format(num_matches)

        d = Context({'user': user_profile,
                     'matches': matches})

        plaintext = get_template('matches_found.txt')
        text_content = plaintext.render(d)

        print 'Emailing {}'.format(user_profile.name)
        try:
            send_mail(title,
                    text_content,
                    'jumbosmashers2@gmail.com',
                    [user_profile.email],
                    fail_silently=False)
        except smptlib.SMTPException:
            print 'Failed to email {}'.format(user_profile.name)
