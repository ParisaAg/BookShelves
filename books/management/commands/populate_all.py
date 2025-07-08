# books/management/commands/populate_all.py

import random
from decimal import Decimal
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from django.db import transaction

# وارد کردن مدل‌ها از هر دو اپلیکیشن
from books.models import Author, Category, Book, Discount
from extra.models import Announcement, Banner

class Command(BaseCommand):
    help = 'Populates the database with fake data. Image fields will contain placeholder URLs.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # --- ۱. پاک کردن تمام داده‌های قدیمی ---
        self.stdout.write('--- Deleting all old data... ---')
        Discount.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()
        Banner.objects.all().delete()
        Announcement.objects.all().delete()

        faker = Faker()

        # --- ۲. ساخت داده‌های اولیه ---
        self.stdout.write('\n--- Creating initial data ---')
        
        self.stdout.write('Creating categories...')
        categories_names = ['Fantasy', 'Science Fiction', 'Mystery', 'Romance', 'Horror', 'Programming', 'Classic']
        categories = [Category.objects.create(name=name) for name in categories_names]

        self.stdout.write('Creating authors...')
        authors = [Author.objects.create(first_name=faker.first_name(), last_name=faker.last_name()) for _ in range(20)]
        
        self.stdout.write('Creating announcements...')
        for _ in range(5):
            Announcement.objects.create(
                message=faker.sentence(nb_words=10),
                link_announce=faker.url()
            )

        # --- ۳. ساخت کتاب‌ها با آدرس عکس ---
        self.stdout.write('\n--- Creating books with placeholder image URLs... ---')
        all_books = []
        for i in range(50): # تعداد کتاب‌ها
            book = Book.objects.create(
                title=' '.join(faker.words(nb=random.randint(2, 5))).title(),
                author=random.choice(authors),
                category=random.choice(categories),
                description=faker.paragraph(nb_sentences=8),
                published_year=random.randint(1980, 2025),
                price=Decimal(random.uniform(10, 150)).quantize(Decimal("0.01")),
                inventory=random.randint(0, 50),
                # مستقیم یک آدرس URL به فیلد عکس می‌دهیم
                cover_image=f'https://picsum.photos/400/600?random=book{i}'
            )
            all_books.append(book)
            self.stdout.write(f'  - Created book: "{book.title}"')

        # --- ۴. ساخت تخفیف‌ها و اتصال به کتاب‌ها ---
        self.stdout.write('\n--- Creating discounts and assigning to books ---')
        now = timezone.now()
        if all_books:
            summer_sale = Discount.objects.create(
                name="Summer Sale",
                discount_percent=20,
                start_date=now,
                end_date=now + timezone.timedelta(days=30),
                is_active=True
            )
            sample_size = min(len(all_books), 10)
            summer_sale.books.set(random.sample(all_books, k=sample_size))
            self.stdout.write(f'  - "Summer Sale" discount created and applied to {sample_size} books.')

        # --- ۵. ساخت بنرها با آدرس عکس ---
        self.stdout.write('\n--- Creating banners with placeholder image URLs ---')
        for i in range(4): # تعداد بنرها
            Banner.objects.create(
                title=' '.join(faker.words(nb=3)).title(),
                subtitle=faker.sentence(nb_words=7),
                button_text="Shop Now",
                button_link="/books/",
                is_active=True,
                # مستقیم یک آدرس URL به فیلد عکس می‌دهیم
                image_url=f'https://picsum.photos/1200/400?random=banner{i}'
            )
            self.stdout.write(f'  - Created banner: "Banner {i+1}"')

        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated all data!'))