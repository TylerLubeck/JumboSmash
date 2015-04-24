import os
import json
from django.core.management.base import BaseCommand, CommandError
from smashers.models import UserProfile

class Command(BaseCommand):
    help = 'Loads the seniors from the json returned by the scraper'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str)

    def handle(self, *args, **options):
        file_name = options['input_file']
        if not os.path.isfile(file_name):
            raise CommandError('{} not found'.format(file_name))

        with open(file_name, 'r') as f:
            seniors = json.load(f)

        for senior in seniors:
            email = senior.get('email', None)
            if email is not None and not UserProfile.objects.filter(email=email).exists():
                UserProfile.objects.create(**senior)

