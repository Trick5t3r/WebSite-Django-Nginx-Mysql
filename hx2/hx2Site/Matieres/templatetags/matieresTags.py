from django import template

register = template.Library()


@register.filter
def sort_list(lst):
        return sorted(lst)

