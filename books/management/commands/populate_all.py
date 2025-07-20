from django.core.management.base import BaseCommand
from books.models import Category, Author, Book, Discount
from faker import Faker
import random
from decimal import Decimal

fake = Faker('fa_IR')  # فارسی

class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        Category.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        Discount.objects.all().delete()

        categories = []
        for _ in range(5):
            cat = Category.objects.create(
                name=fake.word(),
                subtitle=fake.sentence(),
                description=fake.text(),
                is_active=True
            )
            categories.append(cat)

        authors = []
        for _ in range(5):
            author = Author.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text()
            )
            authors.append(author)

        books = []
        for _ in range(20):
            book = Book.objects.create(
                title=fake.sentence(nb_words=4),
                is_available=True,
                inventory=random.randint(0, 50),
                author=random.choice(authors),
                description=fake.text(),
                published_year=random.randint(1990, 2024),
                category=random.choice(categories),
                num_pages=random.randint(100, 1000),
                language="فارسی",
                publisher=fake.company(),
                price=Decimal(random.randint(50000, 300000)),
                book_type=random.choice(['physical', 'digital', 'both']),
                level=random.choice(['beginner', 'intermediate', 'advanced']),
            )
            books.append(book)

        for _ in range(3):
            discount = Discount.objects.create(
                name=fake.word(),
                discount_percent=random.randint(10, 50),
                start_date=fake.date_time_this_year(),
                end_date=fake.date_time_this_year(),
                is_active=True,
            )
            discount.books.set(random.sample(books, k=5))

        self.stdout.write(self.style.SUCCESS("✅ Done seeding data."))
