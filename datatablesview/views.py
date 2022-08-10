from django.shortcuts import render, redirect
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.views import View
from datatablesview.forms import DataTablesFilterForm
from copy import copy
import pdb


class DataTablesView(View):
    title = 'Title here'
    template_name = 'datatablesview/datatablesview.html'
    login_required = True
    permission_name = None
    include_header_partial = None
    columns = []
    filters = []
    not_ordering = []
    page_length = 50
    searching = True

    def get_columns(self, request):
        return self.columns

    def get_result_list(self, request):
        filter_params = self.get_filter_params(request)
        order_by = self.get_order_params(request)
        return self.get_queryset(request, filter_params, order_by)

    def get(self, request):
        data_form = self.get_filter_data_form(request)
        filter_form = DataTablesFilterForm(filters=self.filters, initial=self.get_initial_values(), data=data_form)

        result_list = self.get_result_list(request)

        paginator = Paginator(result_list, self.page_length)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total_entries = paginator.count

        footer_totals = self.get_footer_totals(page_obj, total_entries)
        order_by = request.GET.get('o-b-y', '')

        context_data = {
            'page_obj': page_obj, 'paginator': paginator, 'title': self.title, 'columns': self.columns, 'filters': self.filters,
            'page_length': self.page_length, 'total_entries': total_entries, 'searching': self.searching, 'bold_columns': self.get_bold_columns(),
            'filter_form': filter_form, 'footer_totals': footer_totals, 'include_header_partial': self.include_header_partial, 'o': order_by,
            'not_ordering': self.not_ordering
        }

        return render(request, self.template_name, context_data)

    def dispatch(self, *args, **kwargs):
        if self.login_required and not self.request.user.is_authenticated:
            return redirect('admin:index')

        if self.permission_name is not None and not self.request.user.has_perm(self.permission_name):
            raise PermissionDenied

        return super().dispatch(*args, **kwargs)

    def get_bold_columns(self):
        targets = []
        key = int(1)
        for column in self.columns:
            if column.get('bold_col') == True:
                targets.append(f'{key}')
            key += 1

        return targets

    def get_footer_totals(self, page_obj, total_entries):
        totals = []
        for key, column in enumerate(self.columns):
            if column.get('footer_totals'):
                totals.append({'field': column['field'], 'total': 0, 'index': key, 'type': column.get('footer_totals')})

        if len(totals) > 0:
            for obj in page_obj:
                for total in totals:
                    total['total'] += obj.get(total['field'])

            for total in totals:
                if total['type'] == 'avg':
                    if total_entries > 0:
                        total['total'] = (total['total'] / total_entries).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

        return totals

    def get_filter_data_form(self, request):
        data_form = {}
        for filter in self.filters:
            if filter['type'] == 'date_range':
                field_name_start = f"{filter['field']}_start"
                field_name_end = f"{filter['field']}_end"
                if request.GET.get(field_name_start) or request.GET.get(field_name_end):
                    data_form.update({field_name_start: request.GET.get(field_name_start), field_name_end: request.GET.get(field_name_end)})
            else:
                if request.GET.get(filter['field']):
                    data_form.update({filter['field']: request.GET.get(filter['field'])})

        return data_form if len(data_form) > 0 else None

    def get_filter_params(self, request):
        params = {}
        filter_dates = get_filter_dates()

        for filter in self.filters:
            if filter['type'] == 'date_range':
                try:
                    field_name_start = f"{filter['field']}_start"
                    field_name_end = f"{filter['field']}_end"
                    start_date = datetime.strptime(request.GET.get(field_name_start), '%Y-%m-%d')
                    end_date = datetime.strptime(request.GET.get(field_name_end), '%Y-%m-%d')

                except Exception:
                    start_date = filter_dates[filter['initial']]['start']
                    end_date = filter_dates[filter['initial']]['end']

                params.update({field_name_start: start_date, field_name_end: end_date})

            else:
                params.update({filter['field']: request.GET.get(filter['field'])})
        return params

    def get_order_params(self, request):
        order = request.GET.get('o-b-y')
        if order is None or order == '':
            return {}

        order_by = []
        column_number = int(order.replace('-', ''))

        for key, column in enumerate(self.columns):
            if int(key) == column_number:
                order_mode = column['field']
                if '-' in order:
                    order_mode = f"-{column['field']}"
                order_by.append(order_mode)

        return order_by

    def get_initial_values(self):
        initial = {}
        filter_dates = get_filter_dates()

        for filter in self.filters:
            if filter['type'] == 'date_range' and filter.get('initial') is not None:
                field_name_start = f"{filter['field']}_start"
                field_name_end = f"{filter['field']}_end"
                start_date = filter_dates[filter['initial']]['start'].strftime("%Y-%m-%d")
                end_date = filter_dates[filter['initial']]['end'].strftime("%Y-%m-%d")
                initial.update({field_name_start: start_date, field_name_end: end_date})

            elif filter.get('initial') is not None:
                initial.update({filter['field']: filter.get('initial')})

        return initial


def get_filter_dates():
    now = timezone.now()
    today = date.today()

    first_day_current_month = date.today().replace(day=1)
    last_day_current_month = get_last_day_of_month(now)

    first_day_next_month = first_day_current_month + relativedelta(months=1)
    last_day_next_month = get_last_day_of_month(first_day_next_month)

    last_day_last_month = date(now.year, now.month, 1) - timedelta(1)
    first_day_last_month = last_day_last_month.replace(day=1)

    last_30_days = date.today() - timedelta(days=30)
    last_60_days = date.today() - timedelta(days=60)
    last_90_days = date.today() - timedelta(days=90)
    last_180_days = date.today() - timedelta(days=180)
    last_365_days = date.today() - timedelta(days=365)

    first_day_platform = datetime.strptime('2018-02-01', '%Y-%m-%d')

    dates = {}
    dates['current_month'] = {'start': first_day_current_month, 'end': last_day_current_month}
    dates['next_month'] = {'start': first_day_next_month, 'end': last_day_next_month}
    dates['last_month'] = {'start': first_day_last_month, 'end': last_day_last_month}
    dates['full_period'] = {'start': first_day_platform, 'end': today}
    dates['last_30_days'] = {'start': last_30_days, 'end': today}
    dates['last_60_days'] = {'start': last_60_days, 'end': today}
    dates['last_90_days'] = {'start': last_90_days, 'end': today}
    dates['last_180_days'] = {'start': last_180_days, 'end': today}
    dates['last_365_days'] = {'start': last_365_days, 'end': today}

    return dates


def get_last_day_of_month(date_value):
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])