from django import template

register = template.Library()

@register.filter()
def naira(value):
    """Format value as Naira."""
    return f"₦{value:,.2f}"

# register.filter('naira',naira)
