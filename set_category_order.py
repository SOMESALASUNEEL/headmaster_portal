import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headmasters_portal.settings')
django.setup()

from core.models import Category

def set_category_order():
    """Set default order values for existing categories"""
    categories = Category.objects.all().order_by('name')

    print("Current categories:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.name} (current order: {category.order})")

    print("\nSetting order values based on alphabetical order...")
    for i, category in enumerate(categories, 1):
        category.order = i * 10  # Use multiples of 10 to allow easy reordering
        category.save()
        print(f"Set {category.name} order to {category.order}")

    print("\nOrder values have been set. You can now modify them in the Django admin.")

if __name__ == "__main__":
    set_category_order()