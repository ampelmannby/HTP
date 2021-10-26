import time
import csv


def date_by_components(date_from_products_file):
    only_date = date_from_products_file.split(' ')[0]
    day, month, year = only_date.split('.')[0], only_date.split('.')[1], only_date.split('.')[2],
    return day, month, year

def iso_datetime_to_unix(iso_datetime):
    """
    Переводит дату-время в формат UNIX ('2021-01-01 12:00:00' -> 1609491600)
    :param iso_datetime: Дата и время в формате '2021-01-01 12:00:00'
    :return: Возвращает время в формате UNIX (int)
    """
    unix_time = int(time.mktime(time.strptime(iso_datetime, '%d.%m.%Y %H:%M:%S')))
    return unix_time

def iso_date_to_unix(date: str):
    input = date+' 00:00:00'
    unix_time = iso_datetime_to_unix(input)
    return unix_time


def read_file_from_access():

    products_array = []
    with open("products.txt", newline='') as source_file:
        reader = csv.reader(source_file, delimiter=";")
        for row in reader:
            products_array.append([str(row[6]),
                                   int(iso_datetime_to_unix(row[6])),
                                   str(row[1]),
                                   str(row[2]),
                                   str(row[3]),
                                   str(row[4]),
                                   int(row[5])])
    return products_array

A = read_file_from_access()
month_dict = {
    "1": ["январь", "января"],
    "2": ["февраль", "февраля"],
    "3": ["март", "марта"],
    "4": ["апрель", "апреля"],
    "5": ["май", "мая"],
    "6": ["июнь", "июня"],
    "7": ["июль", "июля"],
    "8": ["август", "августа"],
    "9": ["сентябрь", "сентября"],
    "10": ["октябрь", "октября"],
    "11": ["ноябрь", "ноября"],
    "12": ["декабрь", "декабря"]
}
first_line_unix = iso_datetime_to_unix(A[0][0])
last_line_unix = iso_datetime_to_unix(A[-1][0])
first_day, first_month, first_year = date_by_components(A[0][0])
last_dat, last_month, last_year = date_by_components(A[-1][0])
print(f"\nВ базе данных {len(A)} строк c {month_dict[first_month][1]} {first_year} года по {month_dict[last_month][0]} "
      f"{last_year} года включительно.")

while True:
    last_year_for_search = int(input('\nЗа какой год ищем статистику? (2008 - 2021): '))
    last_month_for_search = int(input('За сколько месяцев ищем статистику? (1 - 12): '))
    start_current_year = '1.1.' + str(last_year_for_search) + ' 00:00:00'
    end_current_year = '1.' + str(last_month_for_search) + '.' + str(last_year_for_search) + ' 00:00:00'
    current_period_start_unix = iso_datetime_to_unix(start_current_year)
    current_period_end_unix = iso_datetime_to_unix(end_current_year)

    start_previous_year = '1.1.' + str(last_year_for_search - 1) + ' 00:00:00'
    end_previous_year = '1.' + str(last_month_for_search) + '.' + str(last_year_for_search - 1) + ' 00:00:00'
    previous_period_start_unix = iso_datetime_to_unix(start_previous_year)
    previous_period_end_unix = iso_datetime_to_unix(end_previous_year)

    export_current = 0
    export_previous = 0
    if last_month_for_search not in range(1, 13):
        print(f'\nМесяца номер {last_month_for_search} не бывает. Уточните и начните заново.')
    elif first_line_unix > current_period_end_unix > last_line_unix:
        print(f'\nЭтот период ({last_year_for_search}/{last_month_for_search}) отсутствует в базе данных. Уточните и начните заново.')
    else:
        if last_year_for_search == 2008 or last_year_for_search == 2009:
            print(
                f'\nИскать данные за 2008 и 2009 годы не рекомендуется.\n'
                f'За 2008 год данные в базе только с февраля.\nСравнение 2009 к 2008 году будет некорректным.\n '
                f'2008 год вообще не с чем сравнивать.\nУчитывайте это при использовании результата')
        for i in range(len(A)):
            if A[i][2] == '1' and current_period_start_unix <= A[i][1] <= current_period_end_unix:
                export_current += A[i][6]
            if A[i][2] == '1' and previous_period_start_unix <= A[i][1] <= previous_period_end_unix:
                export_previous += A[i][6]

        print(f"\nЭкспорт ПВТ за {last_month_for_search} месяцев {last_year_for_search} года: {'{0:,}'.format(export_current).replace(',', ' ')} долларов США")
        print(f"Экспорт ПВТ за {last_month_for_search} месяцев {last_year_for_search-1} года: {'{0:,}'.format(export_previous).replace(',', ' ')} долларов США")
        print(f'Темп роста: {round((export_current/export_previous*100),1)}%')



