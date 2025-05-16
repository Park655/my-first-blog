from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_list(value):
    if not value:
        return ""
    items = value.strip().split('\n')
    list_items = ''.join(f'<li>{item.strip()}</li>' for item in items if item.strip())
    return mark_safe(f'<ul class="supplement-list">{list_items}</ul>')