import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup_scraper = BeautifulSoup(html, 'lxml')
    pages = soup_scraper.find('dl', class_='f-pagination').find_all('a')[-2].get('href')
    total_pages = pages.split('=')[2]
    return int(total_pages)


def write_csv(data):
    with open('rabota_ua.csv', 'a+') as b:
        writer = csv.writer(b)
        writer.writerow((data['title'],
                         data['salary'],
                         data['company_name']))


def get_page_data(html):
    soup_scraper = BeautifulSoup(html, 'lxml')
    vacancies_list = soup_scraper.find('table', class_='f-vacancylist-tablewrap')

    for vacancy in vacancies_list:
        try:
            title = vacancy.find('h3', class_='fd-beefy-gunso f-vacancylist-vacancytitle').text.strip()
        except:
            title = ''
        try:
            salary = vacancy.find('p', class_='fd-beefy-soldier -price').text.replace(u'\xa0', u' ')
        except:
            salary = ''
        try:
            company_name = vacancy.find('p', class_='f-vacancylist-companyname').text.strip()
        except:
            company_name = ''

        data = {'title': title,
                'salary': salary,
                'company_name': company_name, }

        write_csv(data)


def main():
    print(60 * '=')
    print("Parsing in progress...")
    print(60 * '=')
    url = 'https://rabota.ua/jobsearch/vacancy_list?regionId=4'
    base_url = 'https://rabota.ua/jobsearch/vacancy_list?'
    region_part = "regionId=4"
    query_part = "&pg="
    total_pages = get_total_pages(get_html(url))

    # for i in range(1, total_pages + 1):
    #     url_generated = base_url + region_part + query_part + str(i)
    #     html = get_html(url_generated)
    #     get_page_data(html)
    #     print("{} of {} pages parsed".format(i, total_pages))
    for i in range(1, 4):
        url_generated = base_url + region_part + query_part + str(i)
        html = get_html(url_generated)
        get_page_data(html)
        print('{} of {} pages parsed'.format(i, total_pages))
    print(60 * '=')
    print('Parsing finished! File rabota_ua.csv successfully created.')
    print(60 * '=')


if __name__ == '__main__':
    main()
