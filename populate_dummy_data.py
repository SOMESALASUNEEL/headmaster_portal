import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headmasters_portal.settings')
django.setup()

from core.models import Category, Subcategory, Tag, Document
import random

def create_dummy_data():
    # Create 10 Categories
    categories = []
    category_names = [
        "Mathematics", "Science", "History", "Literature", "Geography",
        "Computer Science", "Art", "Music", "Physical Education", "Languages"
    ]

    for name in category_names:
        category = Category.objects.create(name=name)
        categories.append(category)
        print(f"Created Category: {name}")

    # Create Subcategories for each Category (2 per category)
    subcategories = []
    subcategory_names = ["Beginner", "Intermediate", "Advanced", "Theory", "Practice"]

    for category in categories:
        for i in range(2):
            sub_name = f"{category.name} {random.choice(subcategory_names)}"
            subcategory = Subcategory.objects.create(name=sub_name, category=category)
            subcategories.append(subcategory)
            print(f"Created Subcategory: {sub_name}")

    # Create 20 Tags
    tags = []
    tag_names = [
        "Important", "Review", "New", "Updated", "Draft", "Final",
        "Public", "Private", "Archived", "Featured", "Urgent", "Optional",
        "Beginner", "Intermediate", "Advanced", "Theory", "Practice", "Exam",
        "Homework", "Project"
    ]

    for name in tag_names:
        tag = Tag.objects.create(name=name)
        tags.append(tag)
        print(f"Created Tag: {name}")

    # Create 10 Documents for each Category
    document_titles = [
        "Introduction to {}", "Advanced Topics in {}", "Guide to {}", "Overview of {}",
        "Fundamentals of {}", "Mastering {}", "Essentials of {}", "Complete {} Course",
        "Learning {}", "{} Handbook", "{} Reference", "Practical {}", "{} Notes"
    ]

    descriptions = [
        "This document provides a comprehensive overview of {}.",
        "Learn the basics and advanced concepts of {}.",
        "A detailed guide covering all aspects of {}.",
        "Essential information and resources for {}.",
        "Step-by-step tutorial on {}.",
        "Complete reference material for {}.",
        "Practical examples and exercises for {}.",
        "Theoretical foundations of {}.",
        "Real-world applications of {}.",
        "Study materials and notes on {}."
    ]

    for category in categories:
        category_subcategories = [sub for sub in subcategories if sub.category == category]
        for i in range(10):
            title = random.choice(document_titles).format(category.name)
            description = random.choice(descriptions).format(category.name)
            attachment = f"https://example.com/docs/{category.name.lower().replace(' ', '_')}_{i+1}.pdf"

            document = Document.objects.create(
                category=category,
                subcategory=random.choice(category_subcategories) if category_subcategories else None,
                title=title,
                description=description,
                attachment=attachment
            )

            # Add 2-5 random tags
            selected_tags = random.sample(tags, random.randint(2, 5))
            document.tags.set(selected_tags)

            print(f"Created Document: {title} in {category.name}")

    print("\nDummy data creation completed!")
    print(f"Categories: {Category.objects.count()}")
    print(f"Subcategories: {Subcategory.objects.count()}")
    print(f"Tags: {Tag.objects.count()}")
    print(f"Documents: {Document.objects.count()}")

if __name__ == "__main__":
    create_dummy_data()