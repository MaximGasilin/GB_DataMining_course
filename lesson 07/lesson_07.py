import os
import dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_parse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    dotenv.load_dotenv('.env')
<<<<<<< HEAD
=======
    hash_tags = ['cats']
>>>>>>> origin/lesson_07
    crawl_settings = Settings()
    crawl_settings.setmodule('gb_parse.settings')
    crawl_proc = CrawlerProcess(settings=crawl_settings)
    crawl_proc.crawl(InstagramSpider,
<<<<<<< HEAD
=======
                     tags=hash_tags,
>>>>>>> origin/lesson_07
                     login=os.getenv('INST_LOGIN'),
                     enc_password=os.getenv('INST_PSWD'))
    crawl_proc.start()
