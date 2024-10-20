from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_sorting(context, **kwargs):
    req = context['request'].GET.copy()
    req.pop('page', None)
    req.pop('ordering', None)

    req.update(**kwargs)
    return req.urlencode()
