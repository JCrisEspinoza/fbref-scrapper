from util import requests
from bs4 import BeautifulSoup


def parse_stats(bs_stats):
    stats_arr = bs_stats.select('th') + bs_stats.select('td')
    return {stat['data-stat']: stat.text for stat in stats_arr}


def _get(user_url, table_id):
    user_page = requests.get(user_url).text
    bs_user_page = BeautifulSoup(user_page, 'html.parser')

    stats_models = bs_user_page.find('table', id=table_id)

    if stats_models is None:
        return []
    stats_rows = stats_models.select('#stats')
    return [parse_stats(stat) for stat in stats_rows]


def get(user_url):
    return {
        'basic': _get(user_url, 'stats_standard_dom_lg'),
        'shooting': _get(user_url, 'stats_shooting_dom_lg'),
        'time': _get(user_url, 'stats_playing_time_dom_lg'),
        'misc': _get(user_url, 'stats_misc_dom_lg'),
        'passing': _get(user_url, 'stats_passing_dom_lg'),
        'passing_types': _get(user_url, 'stats_passing_types_dom_lg'),
        'gca': _get(user_url, 'stats_gca_dom_lg'),
        'defense': _get(user_url, 'stats_defense_dom_lg'),
        'possession': _get(user_url, 'stats_possession_dom_lg')
    }
