#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
from pathlib import Path

import pandas as pd
import requests
import numpy as np
import csv
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent

head_hist = ['ID', 'year', 'team', 'country', 'div']
head_id = ['ID', 'name', 'player_page', 'Pos', 'age(at 2022)']


def extractYear(year):
    return float(year.split('-')[0])


def playerPOS(player):
    return player.text.split('\xa0')[1][2:]


def extractInfo_players(csv_id, csv_hist, country, players, start_position=None):
    if start_position is None or start_position < 0:
        start_position = 0

    for player in players[start_position:]:
        if player.find('strong') is not None:
            player_name = player.find('a').getText()
            print(player_name)
            page_players = requests.get('https://fbref.com/' + player.find('a').get('href'))
            soup_pp = BeautifulSoup(page_players.text, 'html.parser')

            content_table = soup_pp.find('table', id="stats_standard_dom_lg")

            if bool(content_table) == 0:
                continue
            else:

                pht = content_table.find_all('tr', id="stats")  # player history table
                for row_year in np.arange(len(pht) - 1, 0, -1):
                    year = pht[row_year].find('th').text

                    if float(extractYear(year)) < 2016:
                        break

                    ligue = pht[row_year].find_all('a')[2]  # la segunda (2) col de la fila row_year de la lista "a"
                    age = pht[len(pht) - 1].find_all('td')[0]
                    team = pht[row_year].find_all('td')[1]
                    div = pht[row_year].find_all('a')[3]

                    csv_hist.writerow([player.find('a').get('href').split('/')[-2],  # ID
                                       year,  # year          #year
                                       team.text,  # team
                                       ligue.getText(),  # ligue         #ligue
                                       div.getText()  # division      #division
                                       ])

                csv_id.writerow([player.find('a').get('href').split('/')[-2],  # ID
                                 player.find('a').getText(),  # name
                                 player.find('a').get('href'),  # page
                                 playerPOS(player),  # position
                                 age.getText()  # age
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

#INICIA PROCESO
if __name__ == '__main__':

    # Parametros de configuracion
    dist_folder = os.path.join(BASE_DIR, 'dist')
    url_root = 'https://fbref.com/en/country/players/'
    all_available_countries = ['BRA/Brazil-Football-players', 'ARG/Argentina-Football-Players']

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
