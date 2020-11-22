import json
import time
import requests


class Parse5KaCatalog:

    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
    }

    def __init__(self, parent_group_code, parent_group_name):
        self.result = {'parent_group_code': parent_group_code, 'parent_group_name': parent_group_name,
                       'producs': []}
        self.products_index = set()
        self.products_url = 'https://5ka.ru/api/v2/special_offers/'
        self.params = {
            'records_per_page': 100,
            'categories': parent_group_code
        }
        self.finished = False

    def launch_parsing(self):
        '''
        Запускает процесс чтения данных (парсинга) по координатам каталога. И выполняется до тех пор,
        пока все данные не будут прочитаны

        :return:
            ничего. Результат формируется в переменной self.result
        '''
        while not self.finished:
            self.parse()
            if not self.finished:
                time.sleep(1)

        if self.finished:
             self.save_result()

    def parse(self):
        prod_url = self.products_url
        params = self.params
        while prod_url:
            response: requests.Response = requests.get(prod_url, params=params, headers=self.headers)
            if response.status_code != 200:
                break

            data = response.json()

            for product in data.get('results', []):
                prod_id = product.get('id', '')

                # Добавление происходит только в том случае, если в индексе такого номера нет
                if prod_id not in self.products_index:
                    try:
                        self.result.get('producs').append(product)
                    except Exception:
                        pass
                    else:
                        # При удачном добавлении нового элемента в результат, добавляем id в индекс,
                        # чтобы в случае повторного чтения при сбое не добавить дубль.986\
                        self.products_index.add(prod_id)

            prod_url = data.get('next')
            if params:
                params = {}

        if not prod_url:
            self.finished = True

    def save_result(self):
        with open(f'data/products/catalog_{self.result.get("parent_group_code")}.json', 'w', encoding='UTF-8') as file:
            json.dump(self.result, file, ensure_ascii=False)

    def __str__(self):
        return str(self.result)



class Parse5Ka:

    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
    }

    def __init__(self):
        self.catalog_index = set()
        self.cat_url = 'https://5ka.ru/api/v2/categories/'
        self.params = {
            'records_per_page': 100,
        }
        self.finished = False

    def launch_parsing(self):
        '''
        Выбирает все каталоги

        :return:
            ничего.
        '''
        while not self.finished:
            self.parse()
            if not self.finished:
                time.sleep(1)

    def parse(self):

        сat_url = self.cat_url
        response: requests.Response = requests.get(сat_url, headers=self.headers)

        if response.status_code != 200:
            return None

        data = response.json()
        try:
            for catalog in data:
                parser = Parse5KaCatalog(catalog.get('parent_group_code', ''), catalog.get('parent_group_name', ''))
                parser.launch_parsing()
        except Exception:
            pass
        else:
            self.finished = True

    def __str__(self):
        return str(self.result)


if __name__ == '__main__':
    site_parser = Parse5Ka()
    site_parser.launch_parsing()