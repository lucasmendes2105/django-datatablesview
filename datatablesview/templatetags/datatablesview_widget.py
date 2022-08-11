from django.template import Library
from django.utils import formats
from copy import copy
import pdb

register = Library()


@register.filter(takes_context=True)
def render_column_value(obj, column):
    if column.get('type') == 'money':
        value = formats.localize(obj.get(column.get('field')))
        return f"R$ {value}"
    if column.get('type') == 'pct':
        value = formats.localize(obj.get(column.get('field')))
        return f"{value}%"
    if column.get('type') == 'date':
        return obj.get(column.get('field')).strftime("%d/%m/%y")
    if column.get('type') == 'datetime':
        return obj.get(column.get('field')).strftime("%d/%m/%y %H:%M")        
    if column.get('type') == 'choices':
        value = obj.get(column.get('field'))        
        return column.get('choices').get(value)

    return obj.get(column.get('field'))


@register.filter(takes_context=True)
def print_value_column(value, column):
    if column.get('type') == 'money':
        value = formats.localize(value)
        return f"R$ {value}"
    if column.get('type') == 'pct':
        value = formats.localize(value)
        return f"{value}%"
    return value


@register.filter(takes_context=True)
def render_page_query_string(page, query_dict):
    query = copy(query_dict)
    query['page'] = page
    return query.urlencode()


"""@register.filter(takes_context=True)
def datatable_order_value(obj, column):
    if column.get('type') in ['money', 'int', 'pct']:
        return str(obj.get(column.get('field')))

    return ''


@register.filter(takes_context=True)
def column_class(column, config):
    if column[0] in config['footer_sum']:
        return 'sum'

    if column[0] in config['footer_avg']:
        return 'avg'

    return ''
"""
