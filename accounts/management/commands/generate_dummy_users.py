from django.core.management.base import BaseCommand
from accounts.models import Account
from faker import Faker
import random
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Generate dummy users and staff for Account model'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of users to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        roles = ['user', 'staff']

        for _ in range(count):
            email = fake.unique.email()
            password = 'test12345'
            role = random.choice(roles)
            is_approved = True if role == 'user' else False
            is_active_staff = True

            # Generate a unique username
            while True:
                username = f"{role}{fake.unique.random_number(digits=6)}"
                if not Account.objects.filter(username=username).exists():
                    break

            if not Account.objects.filter(email=email).exists():
                account = Account.objects.create(
                    email=email,
                    username=username,
                    password=make_password(password),
                    role=role,
                    is_approved=is_approved,
                    is_active_staff=is_active_staff,
                    raw_password=password  # Store plain password for testing
                )
                self.stdout.write(self.style.SUCCESS(
                    f"Created {role}: {email} | username: {username} | password: {password}"
                ))
