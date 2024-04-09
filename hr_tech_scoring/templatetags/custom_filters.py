from django import template

register = template.Library()

@register.filter
def get_item(lst, index):
    try:
        return lst[index]
    except IndexError:
        return ""  # Or any default value you want to return