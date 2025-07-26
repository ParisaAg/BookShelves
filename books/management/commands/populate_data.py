# books/management/commands/populate_data.py

import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Author, Category, Book
from django.db import transaction

class Command(BaseCommand):
    help = 'Populates the database with rich fake data, including images.'

    @transaction.atomic 
    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Book.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()

        faker = Faker()

        self.stdout.write('Creating categories...')
        categories_names = [
            'Fantasy', 'Science Fiction', 'Mystery', 'Romance', 'Horror', 'Thriller',
            'Biography', 'History', 'Programming', 'Classic', 'Poetry', 'Self-Help'
        ]
        categories = [Category.objects.create(name=name) for name in categories_names]

        self.stdout.write('Creating authors...')
        authors_list = []
        for _ in range(25): 
            authors_list.append(
                Author(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    bio=faker.paragraph(nb_sentences=3)
                )
            )
        Author.objects.bulk_create(authors_list)
        all_authors = list(Author.objects.all())

        self.stdout.write('Creating books with images (this may take a while)...')
        all_categories = list(Category.objects.all())
        

        for i in range(50): 
            author = random.choice(all_authors)
            category = random.choice(all_categories)
            
            book = Book(
                title=' '.join(faker.words(nb=random.randint(2, 6))).title(),
                author=author,
                category=category,
                description=faker.paragraph(nb_sentences=10),
                price=Decimal(random.uniform(9.99, 199.99)).quantize(Decimal('0.01')),
                discount_percentage=random.choice([None, 10, 15, 20, 25, 30, 50]),
                published_year=random.randint(1950, 2025),
                inventory=random.randint(0, 200),
                is_available=faker.boolean(chance_of_getting_true=85),
                num_pages=random.randint(80, 1200),
                language=random.choice(['English', 'Persian', 'French', 'German', 'Spanish']),
                publisher=faker.company(),

                cover_image=f'https://picsum.photos/400/600?random={i}'
            )
            book.save()
            self.stdout.write(f'  - Created book: "{book.title}"')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with books and images!'))