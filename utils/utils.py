import datetime


# Проверка введенной задачи на корректность
def validate_task(data: str) -> tuple[str, str] | None:
    validated_data = data.split('-')
    if len(validated_data) == 2:
        return validated_data[0], validated_data[1]
    elif len(validated_data) == 1:
        return validated_data[0], ' '
    return None


# Получение даты истечения для задачи
def get_time_period(category_name: str) -> datetime.timedelta | None:
    if category_name == 'Ежедневные':
        time_period = datetime.timedelta(days=1)
    elif category_name == 'На неделю':
        time_period = datetime.timedelta(weeks=1)
    elif category_name == 'На месяц':
        time_period = datetime.timedelta(days=30)
    elif category_name == 'На год':
        time_period = datetime.timedelta(days=365)
    else:
        time_period = None

    return time_period
