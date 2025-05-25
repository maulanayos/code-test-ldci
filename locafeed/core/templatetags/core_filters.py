from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Split a string by delimiter and return list of parts
    Usage: {{ text|split:"@location" }}
    """
    return value.split(delimiter)

@register.filter
def truncate_location(value):
    """
    Truncate a location name to show only the first two comma-separated segments
    Usage: {{ location.name|truncate_location }}
    """
    parts = value.split(',')
    if len(parts) <= 2:
        return value
    return ','.join(parts[:2])
