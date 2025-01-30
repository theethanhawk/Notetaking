from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Adds a CSS class to Django form fields dynamically"""
    return field.as_widget(attrs={"class": css_class})