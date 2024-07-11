# generate_api_keys.py
from django.core.management.base import BaseCommand
from common.models import APIKey  
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Generate API keys'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Number of API keys to generate',
        )
        parser.add_argument(
            '--activate',
            action='store_true',
            help='Activate generated API keys',
        )

    def handle(self, *args, **options):
        count = options['count']
        activate = options['activate']

        keys_generated = []
        for _ in range(count):
            key = get_random_string(length=40)  # Generate a random key
            api_key = APIKey.objects.create(key=key)

            if activate:
                api_key.active = True
                api_key.save()

            keys_generated.append(api_key.key)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} API key(s):'))
        for key in keys_generated:
            self.stdout.write(self.style.SUCCESS(f'- {key}'))
