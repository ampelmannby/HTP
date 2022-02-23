import csv


class Olds:
    def __init__(self):
        self.unp_list = []
        with open("olds.txt", newline='') as source_file:
            reader = csv.reader(source_file)
            for row in reader:
                self.unp_list.append(row[0])


class Database:
    def __init__(self):
        self.line = []
        self.ex_im = []
        self.unp = []
        self.amount = []
        self.date = []
        self.service_code = []
        self.country_code = []
        with open("products.txt", newline='') as source_file:
            reader = csv.reader(source_file, delimiter=";")
            for row in reader:
                self.line.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                self.ex_im.append(int(row[1]))
                self.unp.append(row[2])
                self.service_code.append(row[3])
                self.country_code.append(row[4])
                self.amount.append(int(row[5]))
                self.date.append(row[6])


def separate_olds_and_news():
    database = Database()
    olds = Olds()
    years = {'2016', '2017', '2018', '2019', '2020', '2021'}
    sum_by_year_olds = dict()
    sum_by_year_news = dict()
    for year in years:
        sum_by_year_olds[year] = 0
        sum_by_year_news[year] = 0
        for i in range(len(database.line)):
            if database.ex_im[i] == 1:
                if year in database.date[i]:
                    if database.unp[i] in olds.unp_list:
                        sum_by_year_olds[year] += database.amount[i]
                    else:
                        sum_by_year_news[year] += database.amount[i]
        print(f'Olds in {year}: {sum_by_year_olds[year]}')
        print(f'News in {year}: {sum_by_year_news[year]}')


if __name__ == '__main__':
    separate_olds_and_news()
