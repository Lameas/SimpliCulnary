import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Category, Product


class Command(BaseCommand):
    help = "Generate fake data for products and categories"

    def handle(self, *args, **options):
        fake = Faker("fr_FR")
        categories = []

        for _ in range(5):
            name = fake.unique.word().capitalize()
            slug = fake.unique.slug()
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name},
            )
            categories.append(category)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Categorie creee: {category.name}"))

        for i in range(20):
            product = Product.objects.create(
                name=fake.sentence(nb_words=3).replace(".", ""),
                description=fake.text(max_nb_chars=250),
                price=Decimal(str(round(random.uniform(10.0, 100.0), 2))),
                stock=random.randint(1, 100),
                category=random.choice(categories),
            )
            self.stdout.write(self.style.SUCCESS(f"Produit cree: {product.name}"))
