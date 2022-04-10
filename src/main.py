#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

head_hist = ['ID', 'Season', 'Squad', 'country', 'div']
head_id = ['ID', 'name', 'player_page', 'Pos', 'age(at 2022)']


def playerPOS(player):
    if len(player.text.split('\xa0')) == 1:
        return ' '
    else:
        return player.text.split('\xa0')[1][2:]


def extractInfo_players(players, start_position=None):
    if start_position is None or start_position < 0:
        start_position = 0

    for player in players[start_position:]:
        user_page = player
        page_players = requests.get(user_page)
        soup_pp = BeautifulSoup(page_players.text, 'html.parser')
        content_table = soup_pp.find('table', id="stats_standard_dom_lg")
        if bool(content_table) == 0:
            continue
        else:
            pht = content_table.find_all('tr', id="stats")  # player history table
            for row_year in np.arange(len(pht) - 1, 0, -1):
                year = pht[row_year].find('th').text

                if float(year.split('-')[0]) < 2016:  # check if on actual season (XXXX - year) (year<2016)
                    break

                ligue = pht[row_year].find_all('a')[2]  # la segunda (2) col de la fila row_year de la lista "a"
                age = pht[len(pht) - 1].find_all('td')[0]
                team = pht[row_year].find_all('td')[1]
                div = pht[row_year].find_all('a')[3]
                print([player.find('a').get('href').split('/')[-2],  # ID
                       year,  # year/season
                       team.text,  # team/squad
                       ligue.getText(),  # ligue/country
                       div.getText()  # division
                       ])

            print([player.find('a').get('href').split('/')[-2],  # ID
                   player.find('a').getText(),  # name
                   player.find('a').get('href'),  # page
                   playerPOS(player),  # position
                   age.getText()  # age at last season
                   ])


def migrate_user(user_info, country_info):
    user = entity.User(**user_info, country=country_info["id"])
    db.session.add(user)
    db.session.commit()


def migrate_country(country_info):
    users = country_info.get('users')
    stats = dict()
    last_keys = 0
    skipped_users = 0
    for user_url in users:
        external_id = scrap.user.external_id_from_slug(user_url)
        user_exists = db.session.query(entity.User).filter_by(external_id=external_id).count() > 0

        if user_exists:
            skipped_users += 1
            continue
        if skipped_users > 0:
            print(f'Skipped Users: {skipped_users}')
            skipped_users = 0
        user_info = scrap.user.get(user_url)
        user_stats = scrap.stats.get(user_url)
        for stat in user_stats:
            stats.update(stat)
        if last_keys != len(stats.keys()):
            print(len(stats.keys()), stats)
            last_keys = len(stats.keys())
        migrate_user(user_info, country_info)


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
