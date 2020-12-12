import re
from scrapy import Selector
from scrapy.loader import ItemLoader

from itemloaders.processors import TakeFirst, MapCompose
from .items import AutoYoulaItem, HHVacancyItem


def get_specifications(itm):
    tag = Selector(text=itm)
    return {tag.xpath('//div[contains(@class, "AdvertSpecs_label")]/text()').get():
                tag.xpath('//div[contains(@class, "AdvertSpecs_data")]//text()').get()}


def get_specifications_out(data):
    result = {}
    for itm in data:
        result.update(itm)
    return result
