from django.core.management.base import BaseCommand
from api.users.models import User


class Command(BaseCommand):
    help = 'Create a demo user with predefined credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='demo',
            help='Username for the demo user (default: demo)'
        )
        parser.add_argument(
            '--email', 
            type=str,
            default='demo@demo.com',
            help='Email for the demo user (default: demo@demo.com)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='12345',
            help='Password for the demo user (default: 12345)'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Check if demo user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Demo user with username "{username}" already exists')
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Demo user with email "{email}" already exists')
            )
            return

        # Create demo user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Demo',
            last_name='User',
            age=30,
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created demo user: {username} (email: {email})'
            )
        )