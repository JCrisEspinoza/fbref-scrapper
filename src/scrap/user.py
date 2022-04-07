import re
import urllib.parse as u
import requests
from bs4 import BeautifulSoup

from util.parse import sanitize_number, sanitize_date


def get(bs_user_page):
    user_model = bs_user_page.find('div', itemtype="https://schema.org/Person")
    offset_location = 2
    name_container = user_model.select(f'p:nth-child({offset_location}) > strong')

    name = name_container[0].text.strip() if len(name_container) > 0 else "position"
    if re.search(r'position', name, flags=re.IGNORECASE) is not None:
        offset_location -= 1
        name = user_model.select('h1[itemprop="name"]')[0].text.strip()

    page = bs_user_page.select('meta[property="og:url"]')[0]["content"]
    print(f"{'FIXED - ' if offset_location < 2 else '        '}{name} - '{page}'")
    external_id_container = bs_user_page.select('input[name="player_id1"]')
    external_id = external_id_container[0]["value"] if len(external_id_container) > 0 else None

    position = user_model.select(f'p:nth-child({offset_location + 1})')[0].text
    if len(user_model.select(f'p:nth-child({offset_location + 1}) > strong')):
        position_label = user_model.select(f'p:nth-child({offset_location + 1}) > strong')[0].text
        position = position.replace(position_label, "").strip()

    image_container = bs_user_page.select('#meta > div.media-item > img')
    image = image_container[0]["src"] if len(image_container) > 0 else ""

    height_container = user_model.select('span[itemprop="height"]')
    height = height_container[0].text if len(height_container) > 0 else None

    weight_container = user_model.select('span[itemprop="weight"]')
    weight = weight_container[0].text if len(weight_container) > 0 else None

    birth_container = user_model.select('span[itemprop="birthDate"]')
    birth_date = ""
    if len(birth_container) > 0:
        row = birth_container[0]
        birth_date = row["data-birth"] if "data-birth" in row else row.text

    birth_place_container = user_model.select('span[itemprop="birthPlace"]')
    birth_place = birth_place_container[0].text if len(birth_place_container) > 0 else ""

    return {
        "active": external_id is not None,
        "name": name,
        "position": position.replace(u'\xa0', ' '),
        "image": image,
        "height": sanitize_number(height),
        "weight": sanitize_number(weight),
        "birth_date": sanitize_date(birth_date),
        "birth_place": birth_place.strip(),
        "url": page,
        "external_id": external_id
    }


def list(url_country):
    site_content = requests.get(url_country).text
    content = BeautifulSoup(site_content, 'html.parser')
    users = map(lambda link: u.urljoin(url_country, link.get("href")), content.select('.section_content > p > a'))
    return [*users]