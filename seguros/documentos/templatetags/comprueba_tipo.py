from django import template
from django.db.models import ImageField

register = template.Library()

@register.filter
def is_imagefield(instance, field_name):
    try:
        field = instance._meta.get_field(field_name)
        return isinstance(field, ImageField)
    except:
        return False
    
@register.filter
def get_tipo_campo(obj, field_name):
    return getattr(obj, field_name)
