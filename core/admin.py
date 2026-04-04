import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Category, Subcategory, Document, Tag, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    ordering = ('order', 'name')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    ordering = ('category__name', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'download_count', 'date_added')
    list_filter = ('category', 'subcategory', 'tags', 'date_added')
    search_fields = ('title', 'description', 'tags__name')
    ordering = ('-date_added',)
    readonly_fields = ('date_added', 'date_updated', 'download_count')
    filter_horizontal = ('tags',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date_sent', 'is_read')
    list_filter = ('subject', 'is_read', 'date_sent')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('date_sent',)
    ordering = ('-date_sent',)

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} message(s) marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"

    @admin.action(description="Export selected messages to CSV")
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_messages.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Subject', 'Message', 'Date Sent', 'Is Read'])
        
        for message in queryset:
            writer.writerow([message.name, message.email, message.subject, message.message, 
                             message.date_sent.strftime("%Y-%m-%d %H:%M:%S"), message.is_read])
        return response

    actions = [mark_as_read, export_to_csv]


# Customize the admin site
admin.site.site_header = "forAPHMs Administration"
admin.site.site_title = "forAPHMs Admin Portal"
admin.site.index_title = "Welcome to forAPHMs Administration"
