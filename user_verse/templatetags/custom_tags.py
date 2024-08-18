import json
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def json_script(data, element_id):
    print(data)
    json_data = json.dumps(data)
    print(json_data)
    return format_html('<script id="{}" type="application/json">{}</script>', element_id, json_data)
