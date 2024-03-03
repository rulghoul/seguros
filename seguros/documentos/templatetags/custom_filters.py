from django import template

register = template.Library()

@register.filter
def get_attr(value, arg):
    """Obtiene un atributo de un objeto por su nombre, pasado como una cadena."""
    return getattr(value, arg, "")
