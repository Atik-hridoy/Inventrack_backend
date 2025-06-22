from django.core.management.base import BaseCommand
from inventory.models import Product, StockTransaction
from django.contrib.auth import get_user_model
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Generate dummy stock transactions for products'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of transactions per product')

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR("No superuser found. Please create one first."))
            return

        products = Product.objects.all()
        transaction_types = ['in', 'out', 'adjust', 'correction']
        count = options['count']

        for product in products:
            for _ in range(count):
                t_type = random.choice(transaction_types)
                # Stock in: positive, Stock out: negative, adjust/correction: random
                if t_type == 'in':
                    qty = random.randint(1, 50)
                elif t_type == 'out':
                    qty = -random.randint(1, 30)
                else:
                    qty = random.randint(-10, 10)
                StockTransaction.objects.create(
                    product=product,
                    transaction_type=t_type,
                    quantity=qty,
                    note=fake.sentence(),
                    performed_by=admin_user
                )
            self.stdout.write(self.style.SUCCESS(f"Generated {count} transactions for {product.name}"))