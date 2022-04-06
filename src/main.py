#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import re
from datetime import datetime

import pandas as pd
import requests
import numpy as np
import csv
from bs4 import BeautifulSoup

import database
import entity
from config import BASE_DIR
from util.parse import sanitize_number, sanitize_date

head_hist = ['ID', 'Season', 'Squad', 'country', 'div']
head_id = ['ID', 'name', 'player_page', 'Pos', 'age(at 2022)']


def checkPlayerActivity(player):
    # print(player.getText().split('\xa0')[0][-4:])
    return float(player.getText().split('\xa0')[0][-4:])


def playerPOS(player):
    if len(player.text.split('\xa0')) == 1:
        return ' '
    else:
        return player.text.split('\xa0')[1][2:]


def get_user_data(bs_user_page):
    user_model = bs_user_page.find('div', itemtype="https://schema.org/Person")
    name = user_model.select('p:nth-child(2) > strong')[0].text
    page = bs_user_page.select('meta[property="og:url"]')[0]["content"]
    print(f"{name}) '{page}'")
    external_id_container = bs_user_page.select('input[name="player_id1"]')
    external_id = external_id_container[0]["value"] if len(external_id_container) > 0 else "-1"

    position = user_model.select('p:nth-child(3)')[0].text
    if len(user_model.select('p:nth-child(3) > strong')):
        position = position.replace(user_model.select('p:nth-child(3) > strong')[0].text, "").strip()

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


def extractInfo_players(csv_id, csv_hist, country, players, start_position=None):
    if start_position is None or start_position < 0:
        start_position = 0

    for player in players[start_position:]:
        # if player.find('strong') is not None:
        if checkPlayerActivity(player) > 2016:

            user_page = 'https://fbref.com/' + player.find('a').get('href')
            page_players = requests.get(user_page)
            soup_pp = BeautifulSoup(page_players.text, 'html.parser')
            content_table = soup_pp.find('table', id="stats_standard_dom_lg")
            user_data = get_user_data(soup_pp)
            user = entity.User(**user_data, country=country)
            database.session.add(user)
            database.session.commit()
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
                    csv_hist.writerow([player.find('a').get('href').split('/')[-2],  # ID
                                       year,  # year/season
                                       team.text,  # team/squad
                                       ligue.getText(),  # ligue/country
                                       div.getText()  # division
                                       ])

                csv_id.writerow([player.find('a').get('href').split('/')[-2],  # ID
                                 player.find('a').getText(),  # name
                                 player.find('a').get('href'),  # page
                                 playerPOS(player),  # position
                                 age.getText()  # age at last season
                                 ])


def find_lastIndex(csvfile, list_):
    data = pd.read_csv(csvfile)
    last = data.iloc[len(data) - 1]['player_page']
    i = 0
    for l in list_:
        i = i + 1
        if l.find('a').get('href') == last:
            return i
            break


if __name__ == '__main__':
    # Parametros de configuracion
    dist_folder = os.path.join(BASE_DIR, 'dist')
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)
    entity.sync()
    url_root = 'https://fbref.com/en/country/players/'
    all_available_countries = ['BRA/Brasil-Football-players']  # , 'ARG/Argentina-Football-Players']

    for url_country in all_available_countries:

        country_id = url_country.split('/')[0].lower()
        country_folder = os.path.join(dist_folder, country_id)
        country_file = os.path.join(country_folder, f'{country_id}.country.html')

        # Inicializar directorios si no existen
        if not os.path.exists(country_folder):
            os.makedirs(country_folder)

        # Lectura de datos
        if os.path.exists(country_file):
            with open(country_file, 'r', encoding='utf-8') as f:
                page_content = f.read()
        else:
            page_response = requests.get(url_root + url_country)
            page_content = page_response.text
            with open(country_file, 'w', encoding='utf-8') as f:
                file = f.write(page_content)

        # Cargando datos en memoria
        soup = BeautifulSoup(page_content, 'html.parser')

        players_list = soup.find("div", class_="section_content").find_all('p')

        # Procesando jugadores
        player_file = os.path.join(country_folder, f'{country_id}.players.csv')
        player_info_file = os.path.join(country_folder, f'{country_id}.hist.csv')

        last_row = -1
        open_files = []
        # Crear archivos para almacenar datos
        if os.path.exists(player_file):
            f = open(player_file, 'a+', encoding='utf-8')
            player_csv = csv.writer(f)
            last_row = find_lastIndex(player_file, players_list)
            open_files.append(f)
        else:
            f = open(player_file, 'w', encoding='utf-8')
            player_csv = csv.writer(f)
            player_csv.writerow(head_id)
            open_files.append(f)

        if os.path.exists(player_info_file):
            f = open(player_info_file, 'a+', encoding='utf-8')
            player_info_csv = csv.writer(f)
            open_files.append(f)
        else:
            f = open(player_info_file, 'w', encoding='utf-8')
            player_info_csv = csv.writer(f)
            player_info_csv.writerow(head_hist)
            open_files.append(f)

        extractInfo_players(player_csv, player_info_csv, country_id, players_list, last_row + 1)
        for f in open_files:
            f.close()

#
# print('https://fbref.com/' + player.find('a').get('href') + '-Domestic-League-Stats')
#            pdtable = pd.read_html('https://fbref.com/' + player.find('a').get('href') + '-Domestic-League-Stats') #,attrs = {'id': 'stats_standard_dom_lg'})
#            n_columns=[]
#            [n_columns.append(column[1]) for column in pdtable[0].columns]  # fix columns name
#            pdtable[0].columns = n_columns
#
#
#            if len(pdtable[0]) == 0:
#                continue
#            else:
#
#                for row_year in range(0,len(pdtable[0])-1):
#                    print('dim',len(pdtable[0]))
#                    if pdtable[0].loc[row_year,'Season'] == 'nan':
#                       continue
#                    else:
#                        year = pdtable[0].loc[row_year,'Season']
#                        print(year)
#                        if float(year.split('-')[0]) < 2016:              # check if actual season (XXXX - year) (year<2016)
#                            break
#
#                        age = pdtable[0].loc[row_year,'Age']
#                        team = pdtable[0].loc[row_year,'Squad']
#                        country = pdtable[0].loc[row_year,'Country']
#                        div = pdtable[0].loc[row_year,'Comp']
#
#                        csv_hist.writerow([player.find('a').get('href').split('/')[-2], # ID
#                                           year,                                        # year/season
#                                           team,                                        # team/squad
#                                           country,                                     # ligue/country
#                                           div                                          # division
#                                           ])
#
#
#                csv_id.writerow([player.find('a').get('href').split('/')[-2],   # ID
#                                 player.find('a').getText(),                    # name
#                                 player.find('a').get('href'),                  # page
#                                 playerPOS(player),                             # position
#                                 age                                            # age at last season
#                                 ])
#
