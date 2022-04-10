from util import requests
from bs4 import BeautifulSoup

from util.parse import sanitize_number, sanitize_date


def parse_stats(bs_stats):
    stats_arr = bs_stats.select('th') + bs_stats.select('td')
    return {stat['data-stat']: stat.text for stat in stats_arr}


def get(user_url):
    user_page = requests.get(user_url).text
    bs_user_page = BeautifulSoup(user_page, 'html.parser')

    stats_models = bs_user_page.find('table', id='stats_standard_dom_lg')

    if stats_models is None:
        return []
    stats_rows = stats_models.select('#stats')
    return [parse_stats(stat) for stat in stats_rows]
