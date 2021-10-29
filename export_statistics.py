import time
import csv


class ExportDatabase:

    def __init__(self):
        self.products_worldwide_array = list()
        self.products_of_country_dict = dict()
        self.countries_array = list()
        self.countries_dict = dict()
        self.countries_id_list = list()

        with open("countries.txt", newline='') as source_file:
            reader = csv.reader(source_file, delimiter=";")
            for row in reader:
                self.countries_array.append([str(row[1]), int(row[0])])
            for i in range(len(self.countries_array)):
                self.countries_dict[self.countries_array[i][0]] = self.countries_array[i][1]
                self.countries_id_list.append(int(self.countries_array[i][1]))

        with open("products.txt", newline='') as source_file:
            reader = csv.reader(source_file, delimiter=";")
            for row in reader:
                self.products_worldwide_array.append([int(iso_datetime_to_unix(row[6])), str(row[6]), str(row[1]),
                                                      str(row[2]), str(row[3]), str(row[4]), int(row[5])])
            self.products_worldwide_array.sort()
        for country_id in self.countries_id_list:
            temp_array = []
            for i in range(len(self.products_worldwide_array)):
                if self.products_worldwide_array[i][2] == '1' and int(self.products_worldwide_array[i][5]) == country_id:
                    temp_array.append(self.products_worldwide_array[i])
            self.products_of_country_dict[country_id] = temp_array


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
    input_datetime = date+' 00:00:00'
    unix_time = iso_datetime_to_unix(input_datetime)
    return unix_time


def read_file_products_from_access():

    products_array = []
    with open("products.txt", newline='') as source_file:
        reader = csv.reader(source_file, delimiter=";")
        for row in reader:
            products_array.append([
                int(iso_datetime_to_unix(row[6])),
                    str(row[6]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3]),
                    str(row[4]),
                    int(row[5])
            ])
    return products_array


def separate_product_array_for_countries(products_array, country_id: int):
    products_to_country_array = list()
    for i in range(len(products_array)):
        if products_array[i][2] == '1' and products_array[i][4] == country_id:
            products_to_country_array.append(int(products_array[i][5]))
    return products_to_country_array


def main():
    print('\nПодгружаем необходимые данные...')
    database = ExportDatabase()
    month_dict = {"1": ["январь", "января"], "2": ["февраль", "февраля"], "3": ["март", "марта"],
                      "4": ["апрель", "апреля"],
                      "5": ["май", "мая"], "6": ["июнь", "июня"], "7": ["июль", "июля"], "8": ["август", "августа"],
                      "9": ["сентябрь", "сентября"], "10": ["октябрь", "октября"], "11": ["ноябрь", "ноября"],
                      "12": ["декабрь", "декабря"]}



    while True:
        print('\nИтоги экспорта в какую страну Вас интересуют?'
              '\nВведите страну по-русски или нажмите "Enter" для получения общих данных за весь мир.')
        country_input = input()
        if country_input not in database.countries_dict and country_input != '':
            print('\nТакой страны в базе нет. Уточните.\n')
        else:
            if country_input in database.countries_dict:
                country_id = int(database.countries_dict[country_input])
                print(f'\nИщем статистику по стране: {country_input} (код ISO {country_id}).')
                message = f'Данные по экспорту в страну: {country_input} (код ISO {country_id}).'
                products_array = database.products_of_country_dict[country_id]
                percent_insert = True
            elif country_input == '':
                products_array = database.products_worldwide_array
                print('Ищем статистику за весь мир.')
                message = f'Общие данные экспорту во все страны мира.'
                percent_insert = False
            first_line_unix = products_array[0][0]
            last_line_unix = products_array[-1][0]
            first_day, first_month, first_year = date_by_components(products_array[0][1])
            last_date, last_month, last_year = date_by_components(products_array[-1][1])
            print(f"\nВ базе данных {len(database.products_worldwide_array)} строк c {month_dict[first_month][1]} "
                  f"{first_year} года по {month_dict[last_month][0]} {last_year} года включительно."
                  f"\nДанные этой базы отличаются от эталонных на 2-3%."
                  f"\nЭталонные данные (поквартальные) доступны в отделе мониторинга.")
            last_year_for_search = int(input('\nЗа какой год ищем статистику? (2008 - 2021): '))
            last_month_for_search = int(input('За сколько месяцев ищем статистику? (1 - 12): '))
            start_current_year = '1.1.' + str(last_year_for_search) + ' 00:00:00'
            end_current_year = '1.' + str(last_month_for_search) + '.' + str(last_year_for_search) + ' 00:00:00'
            if last_month_for_search in range(1, 13) and 2005 <= last_year_for_search < 2050:
                current_period_start_unix = iso_datetime_to_unix(start_current_year)
                current_period_end_unix = iso_datetime_to_unix(end_current_year)
                start_previous_year = '1.1.' + str(last_year_for_search - 1) + ' 00:00:00'
                end_previous_year = '1.' + str(last_month_for_search) + '.' + str(last_year_for_search - 1) + ' 00:00:00'
                previous_period_start_unix = iso_datetime_to_unix(start_previous_year)
                previous_period_end_unix = iso_datetime_to_unix(end_previous_year)
            export_current = 0
            export_previous = 0
            world_export_current = 0
            world_export_previous = 0
            if last_month_for_search not in range(1, 13):
                print(f'\nМесяца номер {last_month_for_search} не бывает. Уточните и начните заново.')
            elif last_year_for_search >= 2050:
                print(f'\nРежим ПВТ действует до 2049 года. Искать данные за {last_year_for_search} год не имеет смысла.')
            elif last_year_for_search < 2005:
                print(f'\nВ {last_year_for_search} году ПВТ еще не было.')
            else:
                if current_period_end_unix > last_line_unix or current_period_end_unix < first_line_unix:
                    print(f'\nЭтот период ({last_year_for_search}/{last_month_for_search}) '
                          f'отсутствует в базе данных. Уточните и начните заново.')
                elif first_line_unix <= current_period_end_unix <= last_line_unix:

                    for i in range(len(products_array)):
                        if products_array[i][2] == '1' and current_period_start_unix <= products_array[i][0] <= \
                                current_period_end_unix:
                            export_current += products_array[i][6]
                        if products_array[i][2] == '1' and previous_period_start_unix <= products_array[i][0] <= \
                                previous_period_end_unix:
                            export_previous += products_array[i][6]

                    for i in range(len(database.products_worldwide_array)):
                        if database.products_worldwide_array[i][2] == '1' and current_period_start_unix <= database.products_worldwide_array[i][0] <= \
                                current_period_end_unix:
                            world_export_current += database.products_worldwide_array[i][6]
                        if database.products_worldwide_array[i][2] == '1' and previous_period_start_unix <= database.products_worldwide_array[i][0] <= \
                                previous_period_end_unix:
                            world_export_previous += database.products_worldwide_array[i][6]

                    if percent_insert == True:
                        current_year_percent = f'({str(round(export_current/world_export_current*100, 1))}% от общего объема)'
                        previous_year_percent = f'({str(round(export_previous / world_export_previous * 100, 1))}% от общего объема)'
                    else:
                        current_year_percent = ''
                        previous_year_percent = ''

                    print(f"\n{message}\nЭкспорт ПВТ за {last_month_for_search} месяцев {last_year_for_search} года: "
                          f"{'{0:,}'.format(export_current).replace(',', ' ')} долларов США",current_year_percent)
                    if export_previous != 0:
                        print(f"Экспорт ПВТ за {last_month_for_search} месяцев {last_year_for_search - 1} года: "
                              f"{'{0:,}'.format(export_previous).replace(',', ' ')} долларов США", previous_year_percent)
                        print(f'Темп роста: {round((export_current / export_previous * 100), 1)}%')
                    else:
                        print('Данные за 2007 год сравнивать не с чем.\nСтатистика за 2006 год в базе отсутствует.')


if __name__ == '__main__':
    main()
