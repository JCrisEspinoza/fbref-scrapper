import urllib.parse as u

from scrap import user


def get(base_url, slug):
    country_id = slug.split('/')[0].lower()
    country_url = u.urljoin(base_url, slug)
    users = user.list(country_url)
    return {
        "url": country_url,
        "slug": slug,
        "id": country_id,
        "users": users
    }
