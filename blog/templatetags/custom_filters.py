from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_list(value):
    # None 또는 빈 문자열 처리
    if not value:
        return ""

    # 문자열이 아니면 str로 변환
    if not isinstance(value, str):
        value = str(value)

    # 줄바꿈 기준 분리
    items = value.strip().split('\n')

    # HTML 리스트 생성
    list_items = ''.join(f'<li>{item.strip()}</li>' for item in items if item.strip())
    return mark_safe(f'<ul class="supplement-list">{list_items}</ul>')
