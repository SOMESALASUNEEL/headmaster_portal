from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']

class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        unique_together = ('name', 'category')

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DocumentManager(models.Manager):
    def popular(self):
        """Return most downloaded documents that have an attachment."""
        return self.filter(attachment__isnull=False).order_by('-download_count')

    def recent(self):
        """Return recently added documents with optimized related lookups."""
        return self.select_related('category', 'subcategory').prefetch_related('tags').order_by('-date_added')

class Document(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    attachment = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = DocumentManager()

    def __str__(self):
        return self.title

    def increment_download_count(self):
        """Increment the download count by 1"""
        self.download_count += 1
        self.save(update_fields=['download_count'])

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('resources', 'Resource Request'),
        ('feedback', 'Feedback'),
        ('partnership', 'Partnership'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.date_sent.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-date_sent']
