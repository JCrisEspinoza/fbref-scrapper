import re
from datetime import datetime


def sanitize_number(string_value):
    return float(re.sub(r'[^\d.]+', '', string_value)) if string_value is not None else None


def sanitize_date(string_value, matcher=None, extractor=None):
    default = matcher is None or extractor is None
    if matcher is None:
        matcher = r'\d{4}-\d{2}-\d{2}'
    if extractor is None:
        extractor = '%Y-%m-%d'
    try:
        date_content = re.search(matcher, string_value).group()
        return datetime.strptime(date_content, extractor)
    except Exception:
        return sanitize_date(string_value, matcher=r'\w+\s+\d+,\s*\d+', extractor='%B %d, %Y') if default else None
