from django import forms
from copy import copy
from dal import autocomplete
import pdb


class DataTablesFilterForm(forms.Form):

    def __init__(self, filters=None, initial_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters = filters
        self.initial_data = initial_data
        self.create_fields()

    def create_fields(self):
        for filter in self.filters:

            attrs = {'class': 'form-control'}
            label = filter['title']
            required = filter.get('required', False)
            params = {}

            if filter['type'] == 'select':
                fieldClass = forms.ChoiceField
                widget = forms.Select(attrs=attrs)
                choices = copy(filter['choices'])
                choices.insert(0, (None, 'Selecione'))
                params['choices'] = choices
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)

            elif filter['type'] == 'autocomplete.ModelSelect2':
                fieldClass = forms.ModelChoiceField
                widget = autocomplete.ModelSelect2(url=filter['url'])
                self.fields[filter['field']] = fieldClass(label=label, queryset=filter['queryset'], widget=widget, required=required, **params)

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

            elif filter['type'] == 'date':
                fieldClass = forms.DateField
                attrs.update({'type': 'date'})
                widget = forms.DateInput(attrs=attrs)
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)

            elif filter['type'] == 'text':
                fieldClass = forms.CharField
                widget = forms.TextInput(attrs=attrs)
                self.fields[filter['field']] = fieldClass(label=label, widget=widget, required=required, **params)
