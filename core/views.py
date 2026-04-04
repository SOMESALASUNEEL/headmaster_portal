from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from .models import Document, Category, Tag, ContactMessage

@cache_page(60 * 15)  # Cache the home page for 15 minutes
def home(request):
    # Get latest 5 documents
    latest_documents = Document.objects.recent()[:5]

    # Get most downloaded 5 documents
    most_downloaded = Document.objects.popular().select_related('category', 'subcategory')[:5]

    # Get all categories with their subcategories and some documents
    categories = Category.objects.prefetch_related(
        'subcategories',
        'subcategories__document_set'
    ).all()

    # For each category, get up to 3 documents from its subcategories
    categories_with_docs = []
    for category in categories:
        docs = Document.objects.recent().filter(category=category)[:3]
        categories_with_docs.append({
            'category': category,
            'documents': docs
        })

    context = {
        'latest_documents': latest_documents,
        'most_downloaded': most_downloaded,
        'categories_with_docs': categories_with_docs,
    }
    return render(request, 'core/home.html', context)

def document_detail(request, pk):
    document = get_object_or_404(Document.objects.recent(), pk=pk)
    # Get related documents from same category
    related_documents = Document.objects.recent().filter(category=document.category).exclude(pk=pk)[:4]
    context = {
        'document': document,
        'related_documents': related_documents,
    }
    return render(request, 'core/document_detail.html', context)

def download_document(request, pk):
    """Handle document downloads and increment download count"""
    document = get_object_or_404(Document, pk=pk)
    if document.attachment:
        document.increment_download_count()
        return redirect(document.attachment)
    else:
        messages.error(request, "This document has no attachment available for download.")
        return redirect('document_detail', pk=pk)

def document_list(request):
    documents = Document.objects.select_related('category', 'subcategory').prefetch_related('tags')

    # Latest 5 documents for featured card
    latest_documents = Document.objects.recent()[:5]

    # Most downloaded documents
    most_downloaded = Document.objects.popular().select_related('category', 'subcategory')[:5]

    # Get all categories in order
    categories = Category.objects.all()

    # Filter by category and tags if provided
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')

    if category_id:
        documents = documents.filter(category_id=category_id)
    if tag_id:
        documents = documents.filter(tags__id=tag_id)

    documents = documents.order_by('-date_added')

    # Pagination: 12 items per page
    paginator = Paginator(documents, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'documents': page_obj,  # Using page_obj transparently for the template list
        'page_obj': page_obj,
        'latest_documents': latest_documents,
        'most_downloaded': most_downloaded,
        'categories': categories,
        'selected_category': category_id,
        'selected_tag': tag_id,
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'core/document_list.html', context)

def search(request):
    query = request.GET.get('q', '')
    documents = Document.objects.select_related('category', 'subcategory').prefetch_related('tags')

    if query:
        # Match the exact phrase
        search_filter = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(subcategory__name__icontains=query)
        )

        # Also match individual words (ignoring very short words to prevent noisy results)
        words = [w for w in query.split() if len(w) > 2]
        if len(words) > 1:
            for word in words:
                search_filter |= (
                    Q(title__icontains=word) |
                    Q(description__icontains=word) |
                    Q(tags__name__icontains=word) |
                    Q(category__name__icontains=word) |
                    Q(subcategory__name__icontains=word)
                )

        documents = documents.filter(search_filter).distinct()

    documents = documents.order_by('-date_added')

    # Pagination for search results
    paginator = Paginator(documents, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'documents': page_obj,
        'page_obj': page_obj,
        'query': query,
        'latest_documents': Document.objects.recent()[:5],
        'most_downloaded': Document.objects.popular().select_related('category', 'subcategory')[:5],
        'categories': Category.objects.all(),
        'all_tags': Tag.objects.all(),
    }
    return render(request, 'core/document_list.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact')

        # Save the contact message
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'core/contact.html')
