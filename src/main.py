#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os.path
import urllib.parse as u

import pandas as pd
import requests
import numpy as np
import csv
from bs4 import BeautifulSoup

import config
import database as db
import entity
import scrap
from config import BASE_DIR

stats_relationships = {
    'basic': entity.stats.BasicStats,
    'misc': entity.stats.MiscStats,
    'time': entity.stats.TimeStats,
    'shooting': entity.stats.ShootingStats
}


def migrate_user(user_info, country_info, user_stats):
    user = entity.User(**user_info, country=country_info["id"])
    db.session.add(user)
    db.session.commit()
    for kind in user_stats:
        model = stats_relationships.get(kind)
        stats = user_stats.get(kind)
        for stat in stats:
            db.session.add(model(**stat, user_id=user.id))
    db.session.commit()


def migrate_country(country_info):
    users = country_info.get('users')
    skipped_users = 0
    stats_data = {}
    for user_url in users:
        external_id = scrap.user.external_id_from_slug(user_url)
        user_exists = db.session.query(entity.User).filter_by(external_id=external_id).count() > 0

        if user_exists:
            skipped_users += 1
            continue
        if skipped_users > 0:
            print(f'\nSkipped Users: {skipped_users}\n')
            skipped_users = 0
        user_info = scrap.user.get(user_url)
        user_stats = scrap.stats.get(user_url)

        for key, val in user_stats.items():
            if key not in stats_data:
                stats_data[key] = {}
            for row in val:
                stats_data[key].update(row)
        migrate_user(user_info, country_info, user_stats)


def initialize_environment():
    dist_folder = os.path.join(BASE_DIR, 'dist')
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)
    entity.sync()


if __name__ == '__main__':
    initialize_environment()
    # Parametros de configuracion
    country_base_domain = u.urljoin(config.FBREF_BASE_URL, config.FBREF_COUNTRY_BASE_SLUG)
    country_data_slugs = config.FBREF_COUNTRIES_TO_SCRAP

    for country_slug in country_data_slugs:
        country = scrap.country.get(country_base_domain, country_slug)
        migrate_country(country)
