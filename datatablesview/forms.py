from django import forms
from copy import copy
from dal import autocomplete
from datatablesview.util import get_filter_dates
import pdb


class DataTablesFilterForm(forms.Form):

    def __init__(self, filters=None, initial_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters = filters
        self.initial_data = initial_data
        self.create_fields()

    def create_fields(self):
        for filter in self.filters:

            attrs = {'class': 'form-control form-control-sm'}
            label = filter['title']
            required = filter.get('required', False)
            if required:
                attrs['class'] += " required"
            params = {}

            if filter['type'] == 'select':
                fieldClass = forms.ChoiceField
                widget = forms.Select(attrs={'class': 'form-select form-select-sm w-100'})
                choices = copy(filter['choices'])
                choices.insert(0, (None, 'Selecione'))
                params['choices'] = choices
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)

            elif filter['type'] == 'autocomplete.ModelSelect2':
                fieldClass = forms.ModelChoiceField
                widget = autocomplete.ModelSelect2(url=filter['url'], attrs={'data-dropdown-parent':'#filterModal'})
                self.fields[filter['field']] = fieldClass(label=label, queryset=filter['queryset'], widget=widget, required=required, **params)

            elif filter['type'] == 'date_range_picker':
                fieldClass = forms.CharField
                attrs.update({'placeholder': 'Selecione um período', 'autocomplete':'off', 'class':'form-control form-control-sm date-range-picker-filter', 'data-range_list': filter.get('range_list'), 'data-apply_action': None})
                widget = forms.TextInput(attrs=attrs)
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)

            elif filter['type'] == 'date_range':
                fieldClass = forms.DateField
                attrs.update({'type': 'date'})
                widget = forms.DateInput(attrs=attrs)
                start_name = f"{filter['field']}_start"
                end_name = f"{filter['field']}_end"
                label_start = f'{label} - De:'
                label_end = f'{label} - Até:'
                self.fields[start_name] = fieldClass(label=label_start, widget=widget, required=required, **params)
                self.fields[end_name] = fieldClass(label=label_end, widget=widget, required=required, **params)

                if filter.get('fast_filter'):
                    fast_filter_name = f"{filter['field']}_fast_filter"
                    attrs_fast_filter = {'fast_filter_list':filter.get('fast_filter'), 'field_name':filter['field']}
                    self.fields[fast_filter_name] = forms.CharField(label='', widget=DateFastFilterInput(attrs=attrs_fast_filter), required=False, **params)

            elif filter['type'] == 'date':
                fieldClass = forms.DateField
                attrs.update({'type': 'date'})
                widget = forms.DateInput(attrs=attrs)
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)

            elif filter['type'] == 'text':
                fieldClass = forms.CharField
                widget = forms.TextInput(attrs=attrs)
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)


class DateFastFilterInput(forms.widgets.Input):
    input_type = 'text'
    template_name = 'datatablesview/date_fast_filter_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['filter_dates'] = get_filter_dates()
        dropdown_list = []

        for filter in context['widget']['attrs']['fast_filter_list']:
            filter_date = context['filter_dates'][filter[0]]
            dropdown_list.append({'filter':filter, 'label':filter[1], 'start':filter_date['start'], 'end':filter_date['end']})

        context['dropdown_list'] = dropdown_list
        return context
