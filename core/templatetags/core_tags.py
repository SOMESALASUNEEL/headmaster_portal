import re
from django import template
from itertools import groupby as itertools_groupby
from operator import attrgetter
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()

@register.filter
def groupby(value, arg):
    """
    Group a list of objects by a common attribute.
    Usage: {% for group in objects|groupby:"attribute" %}
    """
    if not value:
        return []

    def get_sort_key(obj):
        val = attrgetter(arg)(obj)
        if val is None:
            return (0, 0)
        if hasattr(val, 'pk'):
            return (1, val.pk)
        return (2, str(val))

    # Sort the list by the attribute first
    sorted_value = sorted(value, key=get_sort_key)

    # Group by the attribute
    grouped = []
    for key, group_obj in itertools_groupby(sorted_value, key=attrgetter(arg)):
        grouped.append({
            'grouper': key,
            'list': list(group_obj)
        })

    return grouped

@register.filter(name='highlight')
def highlight(text, search_query):
    """Highlights search terms in the given text."""
    if not search_query or not text:
        return text
        
    # Escape the text to prevent XSS injection before making it safe
    text = escape(str(text))
    
    query = search_query.strip()
    words = [query] + [w for w in query.split() if len(w) > 2]
    # Remove duplicates and sort by length descending to match longest phrases first
    words = sorted(list(set(words)), key=len, reverse=True)
    
    if not words or not words[0]:
        return mark_safe(text)
        
    pattern = re.compile(f"({'|'.join(map(re.escape, words))})", re.IGNORECASE)
    highlighted_text = pattern.sub(r'<span class="highlight-match">\1</span>', text)
    return mark_safe(highlighted_text)