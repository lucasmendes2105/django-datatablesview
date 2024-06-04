from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from django.utils import timezone


def get_filter_dates():
    now = timezone.now()
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)

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

    next_60_days = date.today() + timedelta(days=60)
    next_90_days = date.today() + timedelta(days=90)

    first_day_platform = datetime.strptime('2018-02-01', '%Y-%m-%d')

    dates = {}
    dates['today'] = {'start': today, 'end': today}
    dates['tomorrow'] = {'start': tomorrow, 'end': tomorrow}
    dates['yesterday'] = {'start': yesterday, 'end': yesterday}
    dates['current_month'] = {'start': first_day_current_month, 'end': last_day_current_month}
    dates['next_month'] = {'start': first_day_next_month, 'end': last_day_next_month}
    dates['last_month'] = {'start': first_day_last_month, 'end': last_day_last_month}
    dates['full_period'] = {'start': first_day_platform, 'end': today}
    dates['last_30_days'] = {'start': last_30_days, 'end': today}
    dates['last_60_days'] = {'start': last_60_days, 'end': today}
    dates['last_90_days'] = {'start': last_90_days, 'end': today}
    dates['last_180_days'] = {'start': last_180_days, 'end': today}
    dates['last_365_days'] = {'start': last_365_days, 'end': today}
    dates['next_60_days'] = {'start': today, 'end': next_60_days}
    dates['next_90_days'] = {'start': today, 'end': next_90_days}

    return dates


def get_last_day_of_month(date_value):
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1])
