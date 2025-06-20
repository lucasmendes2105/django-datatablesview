from django.template import Library
from django.utils import formats
from babel.numbers import format_currency
from django.utils.formats import number_format
from copy import copy
import pdb

register = Library()


@register.simple_tag(takes_context=True)
def render_column_value(context, obj, column, currency_code, locale):
    if column.get('type') == 'money':
        return format_currency(number=obj.get(column.get('field')), currency=currency_code, locale=locale)

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

    if column.get('type') == 'int':
        return number_format(obj.get(column.get('field')), use_l10n=True, decimal_pos=0)

    return obj.get(column.get('field'))


@register.simple_tag(takes_context=True)
def print_value_column(context, value, column, currency_code, locale):
    if column.get('type') == 'money':
        return format_currency(number=value, currency=currency_code, locale=locale)

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
