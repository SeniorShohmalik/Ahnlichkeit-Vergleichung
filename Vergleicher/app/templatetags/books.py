from django import template
from django.template.defaultfilters import stringfilter
import re
from django.utils.html import mark_safe

register = template.Library()

@register.filter(name='highlight')
@stringfilter
def highlight_keywords(value, keywords):
    """
    Highlight occurrences of multiple keywords in the given text.
    """
    v = value.split()
    text = ' '.join(v)
    for keyword in keywords:
        text = text.replace(
            keyword, f'<span class="highlight">{keyword}</span>'
        )

    return mark_safe(text)