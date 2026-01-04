from django import template

register = template.Library()

@register.filter
def isList(value):
    return isinstance(value, list)

@register.simple_tag
def getCell(value, row, col):
    return value[int(row)][(int(col))]