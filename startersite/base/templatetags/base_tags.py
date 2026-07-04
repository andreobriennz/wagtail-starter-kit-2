import random

from django import template

from wagtail.models import Page


register = template.Library()


@register.simple_tag
def random_int():
    return random.randint(1, 1000000)


@register.simple_tag(takes_context=True)
def get_page_form(context, **kwargs):
    try:
        form_page = Page.objects.get(id=kwargs["form_page_id"]).specific
    except:
        return None
    request = context["request"]
    form = form_page.get_form(page=form_page, user=request.user)

    if form_page and form:
        return {"page": form_page, "form": form}
    else:
        return None


@register.simple_tag(takes_context=True)
def set_breakpoint(context, *args):
    """
    Set breakpoints in the template for easy examination of the context,
    or any variables of your choice.
    Usage:
        {% load breakpoint %}
        {% set_breakpoint %}
              - or -
        {% set_breakpoint your_variable your_other_variable %}
    - The context is always accessible in the pdb console as a dict 'context'.
    - Additional variables can be accessed as vars[i] in the pdb console.
      - e.g. in the example above, your_variable will called vars[0] in the
             console, your_other_variable is vars[1]
    """
    vars = [arg for arg in locals()['args']]  # noqa F841
    breakpoint()
