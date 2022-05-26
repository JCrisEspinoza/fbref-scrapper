import urllib.parse as u
import requests
from bs4 import BeautifulSoup

from util.parse import sanitize_number, sanitize_date


def get(user_url):
    user_page = requests.get(user_url).text
    bs_user_page = BeautifulSoup(user_page, 'html.parser')

    user_model = bs_user_page.find('div', itemtype="https://schema.org/Person")

    if user_model is None:
        return None

    offset_location = 2
    name_container = user_model.select(f'p:nth-child({offset_location}) > strong')

    name = name_container[0].text.strip() if len(name_container) > 0 else "position"
    name_tags = name.lower().split(" ")
    slug_name = user_url.split("/")[-1].lower()
    slug_and_name_correlation = sum(map(lambda tag: slug_name.find(tag) > -1, name_tags))
    if slug_and_name_correlation == 0:
        offset_location -= 1
        name = user_model.select('h1[itemprop="name"]')[0].text.strip()

    print(f"{'FIXED - ' if offset_location < 2 else '        '}{name} - '{user_url}'")
    external_id_container = bs_user_page.select('input[name="player_id1"]')
    external_id = external_id_container[0]["value"] if len(external_id_container) > 0 else external_id_from_slug(
        user_url)

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
        "url": user_url,
        "external_id": external_id
    }


def list(url_country):
    site_content = requests.get(url_country).text
    content = BeautifulSoup(site_content, 'html.parser')
    links = filter(lambda link: link.get("href").find('players') > -1, content.select('.section_content > p > a'))
    return [*map(lambda link: u.urljoin(url_country, link.get("href")), links)]


def external_id_from_slug(user_url):
    return user_url.split('/')[-2]
