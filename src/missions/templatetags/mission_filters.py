from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Sépare une chaîne selon un délimiteur et supprime les espaces autour des éléments"""
    return [item.strip() for item in value.split(delimiter) if item.strip()]