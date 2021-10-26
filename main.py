import time
import csv

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
print(f'\nВ базе данных {len(A)} строк c {A[0][0]} по {A[0][-1]}')

last_year_for_search = int(input('\nЗа какой год ищем статистику? (2008 - 2021): '))
last_month_for_search = int(input('За сколько месяцев ищем статистику? (1 - 12): '))
if last_month_for_search not in range(1, 13) or last_year_for_search not in range(2008, 2022):
    print(f'\nВведен неправильный период поиска статистики. Уточните и начните заново.')
    quit()
else:
    start_current_year = '1.1.' + str(last_year_for_search) +' 00:00:00'
    end_current_year = '1.'+str(last_month_for_search) +'.' + str(last_year_for_search) +' 00:00:00'
    current_period_start = iso_datetime_to_unix(start_current_year)
    current_period_end = iso_datetime_to_unix(end_current_year)

    start_previous_year = '1.1.' + str(last_year_for_search-1) + ' 00:00:00'
    end_previous_year = '1.' + str(last_month_for_search) + '.' + str(last_year_for_search -1) + ' 00:00:00'
    previous_period_start = iso_datetime_to_unix(start_previous_year)
    previous_period_end = iso_datetime_to_unix(end_previous_year)

export_current = 0
export_previous = 0

for i in range(len(A)):
    if A[i][2] == '1' and current_period_start <= A[i][1] <= current_period_end:
        export_current += A[i][6]
    if A[i][2] == '1' and previous_period_start <= A[i][1] <= previous_period_end:
        export_previous += A[i][6]

print(f"\nЭкспорт ПВТ за {last_month_for_search} месяцев {last_year_for_search} года: {'{0:,}'.format(export_current).replace(',', ' ')} долларов США")
print(f"Экспорт ПВТ за {last_month_for_search} месяцев {last_year_for_search-1} года: {'{0:,}'.format(export_previous).replace(',', ' ')} долларов США")
print(f'Темп роста: {round((export_current/export_previous*100),1)}%')



