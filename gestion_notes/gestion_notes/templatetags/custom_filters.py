from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retourne la valeur associée à `key` dans `dictionary`."""
    return dictionary.get(key, "")
