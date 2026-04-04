import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headmasters_portal.settings')
django.setup()

from core.models import Category, Subcategory, Tag, Document

def clear_dummy_data():
    """Delete all dummy data created by populate_dummy_data.py"""

    # Delete all documents first (due to foreign key constraints)
    documents_count = Document.objects.count()
    Document.objects.all().delete()
    print(f"Deleted {documents_count} documents")

    # Delete all tags
    tags_count = Tag.objects.count()
    Tag.objects.all().delete()
    print(f"Deleted {tags_count} tags")

    # Delete all subcategories
    subcategories_count = Subcategory.objects.count()
    Subcategory.objects.all().delete()
    print(f"Deleted {subcategories_count} subcategories")

    # Delete all categories
    categories_count = Category.objects.count()
    Category.objects.all().delete()
    print(f"Deleted {categories_count} categories")

    print("\nAll dummy data has been cleared!")
    print("Remaining counts:")
    print(f"Categories: {Category.objects.count()}")
    print(f"Subcategories: {Subcategory.objects.count()}")
    print(f"Tags: {Tag.objects.count()}")
    print(f"Documents: {Document.objects.count()}")

if __name__ == "__main__":
    clear_dummy_data()