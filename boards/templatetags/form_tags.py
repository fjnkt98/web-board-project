from typing import TYPE_CHECKING

from django import template

if TYPE_CHECKING:
    from django.forms import BoundField

register = template.Library()


@register.filter
def field_type(bound_field: BoundField) -> str:
    """Get the type of the widget of a form field."""
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field: BoundField) -> str:
    """Derive the CSS class for the input element of a form field."""
    css_classes = ["form-control"]
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_classes.append("is-invalid")
        elif field_type(bound_field) != "PasswordInput":
            css_classes.append("is-valid")

    return " ".join(css_classes)
