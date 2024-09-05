from django import template
from itertools import groupby
from operator import attrgetter
from django.db.models import DateField
from django.db.models.functions import TruncDate

register = template.Library()

@register.filter(name='group_by_date')
def group_by_date(posts):
    # Order by date to ensure proper grouping
    posts = sorted(posts, key=attrgetter('created_at'))
    
    # Group by date and convert groups to lists
    grouped = groupby(posts, lambda p: p.created_at.date())
    result = [(date, list(posts_group)) for date, posts_group in grouped]
    result.sort(key=lambda x: x[0], reverse=True)
    return result
    # # Assuming posts are ordered by date
    # grouped = groupby(posts, lambda p: p.created_at.date())
    # return {date: list(posts) for date, posts in grouped}

