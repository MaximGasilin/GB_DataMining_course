import datetime as dt
import json
import scrapy
import requests
<<<<<<< HEAD
from pymongo import MongoClient
=======
>>>>>>> origin/lesson_07
from ..items import InstaTag, InstaPost


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    api_url = '/graphql/query/'
<<<<<<< HEAD
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", }
    params = {}

    query_hash = {
        # 'posts': '56a7068fea504063273cc2120ffd54f3',
        # 'tag_posts': "9b498c08113f1e09617a1703c22b2f32",
        'recommend_friends': "ed2e3ff5ae8b96717476b62ef06ed8cc&variables",
        'user': "d4d88dc1500312af6f937f7b804c68c3",
        'subscribers': "c76146de99bb02f6415203be841dd25a&variables",
        'subscription': "d04b0a864b4b54837c0d870b0e77e076&variables",
    }

    def __init__(self, login, enc_password,  *args, **kwargs):
        self.login = login
        self.enc_passwd = enc_password
        self.db = MongoClient()['parse_13']

=======
    
    query_hash = {
        'posts': '56a7068fea504063273cc2120ffd54f3',
        'tag_posts': "9b498c08113f1e09617a1703c22b2f32",
        'recommend_friends': "ed2e3ff5ae8b96717476b62ef06ed8cc&variables",
        'user': "d4d88dc1500312af6f937f7b804c68c3",
        'subscribers': "c76146de99bb02f6415203be841dd25a&variables",
    }

    def __init__(self, login, enc_password, tags,  *args, **kwargs):
        self.tags = tags
        self.login = login
        self.enc_passwd = enc_password
>>>>>>> origin/lesson_07
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.enc_passwd,
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError as e:
            if response.json().get('authenticated'):
                variables = {
                    'fetch_media_count': 0,
                    'fetch_suggested_count': 30,
                    'ignore_cache': True,
                    'filter_followed_friends': True,
                    'seen_ids': [],
                    'include_reel': True,

                }

                yield response.follow(
                    url=f'{self.api_url}?query_hash={self.query_hash["recommend_friends"]}&variables={json.dumps(variables)}',
                    callback=self.recommened_parse
                )

<<<<<<< HEAD
=======

>>>>>>> origin/lesson_07
    def recommened_parse(self, response):
        variables = {
            'user_id': "",
            'include_chaining': True,
            'include_reel': True,
            'include_suggested_users': False,
            'include_logged_out_extras': False,
            'include_highlight_reels': False,
            'include_live_status': True,

        }
        rf_list = json.loads(response.text)['data']['user']['edge_suggested_users']['edges']
        for rf in rf_list:
            u_id = rf['node']['user']['id']
            u_name = rf['node']['user']['username']
            variables['user_id'] = u_id
<<<<<<< HEAD
            # print(u_id, u_name)
=======
            print(u_id, u_name)
>>>>>>> origin/lesson_07

            yield response.follow(
                url=f'{self.api_url}?query_hash={self.query_hash["user"]}&variables={json.dumps(variables)}',
                callback=self.user_parse
            )

    def user_parse(self, response):
<<<<<<< HEAD

        user_common_date = {}

=======
>>>>>>> origin/lesson_07
        subscribers_variables = {
            'id': "",
            'include_reel': True,
            'fetch_mutual': True,
            'first': 1,
        }

<<<<<<< HEAD
        subscription_variables = {
            'id': "",
            'include_reel': True,
            'fetch_mutual': True,
            'first': 1,
        }

        user_data = json.loads(response.text)

        user_common_date['id'] = user_data['data']['user']['reel']['user']['id']
        user_common_date['username'] = user_data['data']['user']['reel']['user']['username']


        subscribers_variables['id'] = user_common_date['id']
        response_1 = requests.get(
            f'https://www.instagram.com{self.api_url}?query_hash={self.query_hash["subscribers"]}&variables={json.dumps(subscribers_variables)}',
            params=self.params,
            headers=self.headers
        )
        slist_data = json.loads(response_1.text)
        subscribers_variables['first'] = slist_data['data']['user']['edge_followed_by']['count']

        user_common_date['subscribers'] = self.subscribers_parse(requests.get(
            f'https://www.instagram.com{self.api_url}?query_hash={self.query_hash["subscribers"]}&variables={json.dumps(subscribers_variables)}',
            params=self.params,
            headers=self.headers
        ))

        # yield response.follow(
        #     url=f'{self.api_url}?query_hash={self.query_hash["subscribers"]}&variables={json.dumps(subscribers_variables)}',
        #     callback=self.subscribers_parse
        # )

        subscription_variables['id'] = user_data['data']['user']['reel']['id']
        response_2 = requests.get(
            f'https://www.instagram.com{self.api_url}?query_hash={self.query_hash["subscription"]}&variables={json.dumps(subscription_variables)}',
            params=self.params,
            headers=self.headers
        )
        slist_data = json.loads(response_2.text)
        # print(slist_data['data']['user']['edge_followed_by']['count'])
        subscription_variables['first'] = slist_data['data']['user']['edge_follow']['count']

        user_common_date['subscription'] = self.subscription_parse(requests.get(
            f'https://www.instagram.com{self.api_url}?query_hash={self.query_hash["subscription"]}&variables={json.dumps(subscription_variables)}',
            params=self.params,
            headers=self.headers
        ))
        # yield response.follow(
        #     url=f'{self.api_url}?query_hash={self.query_hash["subscription"]}&variables={json.dumps(subscription_variables)}',
        #     callback=self.subscription_parse
        # )
        collection = self.db['Instagramm']
        collection.insert_one(user_common_date)
=======
        user_data = json.loads(response.text)
        subscribers_variables['id'] = user_data['data']['user']['reel']['id']
        response_1 = scrapy.Request(
            f'{self.start_urls[0]}{self.api_url}?query_hash={self.query_hash["subscribers"]}&variables={json.dumps(subscribers_variables)}')
        slist_data = json.loads(response_1.text)
        print(slist_data['data']['user']['edge_followed_by']['count'])
        subscribers_variables['first'] = slist_data['data']['user']['edge_followed_by']['count']

        yield response.follow(
            url=f'{self.api_url}?query_hash={self.query_hash["subscribers"]}&variables={json.dumps(subscribers_variables)}',
            callback=self.subscribers_parse
        )

>>>>>>> origin/lesson_07

    def subscribers_parse(self, response): # список подпсчиков
        result = []
        user_data = json.loads(response.text)
        for el in user_data['data']['user']['edge_followed_by']['edges']:
<<<<<<< HEAD
            result.append({'id': el['node']['id'], 'username': el['node']['username'], 'full_name': el['node']['full_name']})

        return result
        # print(result)

    def subscription_parse(self, response): # список подпсок
        result = []
        user_data = json.loads(response.text)
        for el in user_data['data']['user']['edge_follow']['edges']:
            result.append({'id': el['node']['id'], 'username': el['node']['username'], 'full_name': el['node']['full_name']})

        return result
        # print(result)
=======
            result.append(el[{'id': el['id'], 'username': el['username'], 'full_name': el['full_name']}])

        print(result)

    def tag_parse(self, response):

        for rec_friend in response.xpath(self._xpath['recommend_friends']):
            yield response.follow(pag_page, callback=self.parse)

        tag = self.js_data_extract(response)['entry_data']['TagPage'][0]['graphql']['hashtag']

        yield InstaTag(
            date_parse=dt.datetime.utcnow(),
            data={
                'id': tag['id'],
                'name': tag['name'],
                'profile_pic_url': tag['profile_pic_url'],
            }
        )
        yield from self.get_tag_posts(tag, response)

    def tag_api_parse(self, response):
        yield from self.get_tag_posts(response.json()['data']['hashtag'], response)

    def get_tag_posts(self, tag, response):
        if tag['edge_hashtag_to_media']['page_info']['has_next_page']:
            variables = {
                'tag_name': tag['name'],
                'first': 100,
                'after': tag['edge_hashtag_to_media']['page_info']['end_cursor'],
            }
            url = f'{self.api_url}?query_hash={self.query_hash["tag_posts"]}&variables={json.dumps(variables)}'
            yield response.follow(
                url,
                callback=self.tag_api_parse,
            )

        yield from self.get_post_item(tag['edge_hashtag_to_media']['edges'])

    @staticmethod
    def get_image_from_insta(display_url, id):
        response_img: requests.Response = requests.get(display_url)
        if response_img.status_code != 200:
            pass
        else:
            with open(f"images/{id}.jpg", "wb") as out_file:
                out_file.write(response_img.content)

    @staticmethod
    def get_post_item(edges):
        for node in edges:
            InstagramSpider.get_image_from_insta(node['node']['display_url'], node['node']['id'])
            yield InstaPost(
                date_parse=dt.datetime.utcnow(),
                data=node['node']
            )
>>>>>>> origin/lesson_07

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace("window._sharedData =", '')[:-1])
<<<<<<< HEAD
=======


>>>>>>> origin/lesson_07
