#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import requests
import numpy as np
import csv
from bs4 import BeautifulSoup


def extractYear(year):
    return float(year.split('-')[0])


def playerPOS(player):
    return player.text.split('\xa0')[1][2:]


def extractInfo_players(csv_id, csv_hist, country, players):
    for player in players:
        if player.find('strong') is not None:

            print(player.getText())
            page_players = requests.get('https://fbref.com/' + player.find('a').get('href'))
            soup_pp = BeautifulSoup(page_players.text, 'html.parser')

            # frontTable = soup_pp.find_all('div',id="meta")
            contentTable = soup_pp.find('table', id="stats_standard_dom_lg")

            if bool(contentTable) == 0:
                continue
            else:

                pht = contentTable.find_all('tr', id="stats")  # player history table
                for row_year in np.arange(len(pht) - 1, 0, -1):
                    year = pht[row_year].find('th').text

                    if float(extractYear(year)) < 2016:
                        break

                    ligue = pht[row_year].find_all('a')[2]  # la segunda (2) col de la fila row_year de la lista "a"
                    age = pht[len(pht) - 1].find_all('td')[0]
                    team = pht[row_year].find_all('td')[1]
                    div = pht[row_year].find_all('a')[3]
                    print(team.text)

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
    print('ultimo registro:', last)
    i = 0
    for l in list_:
        i = i + 1
        if l.find('a').get('href') == last:
            return i
            break


if __name__ == '__main__':

    # db.Base.metadata.create_all(db.engine)

    url_root = 'https://fbref.com/en/country/players/'
    url_country = 'ARG/Argentina-Football-Players'  # 'div_8236552747')
    # url_country  = 'BRA/Brazil-Football-Players'

    try:
        # busca archivo html en carpeta
        with open(url_country[:3] + '_HTML', 'r') as f:
            file = f.read()
        soup = BeautifulSoup(file, 'html.parser')
    except FileNotFoundError:
        # abre y escribe en archivo y solicita url
        page = requests.get(url_root + url_country)
        soup = BeautifulSoup(page.text, 'html.parser')
        with open(url_country[:3] + '_HTML', 'w') as f:
            file = f.write(str(soup))

    players_list = soup.find("div", class_="section_content").find_all('p')
    head_hist = ['ID', 'year', 'team', 'country', 'div']
    head_id = ['ID', 'name', 'player_page', 'Pos', 'age(at 2022)']

    try:
        with open(url_country[:3] + 'players_ID.csv', 'a+') as file_id, open(url_country[:3] + 'players_hist.csv',
                                                                             'a+') as file_hist:
            csv_hist = csv.writer(file_hist)
            csv_id = csv.writer(file_id)

            N = find_lastIndex(url_country[:3] + 'players_ID_c.csv', players_list)
            print('N=', N)
            extractInfo_players(csv_id, csv_hist, url_country[:3], players_list[N + 1:])
    except FileNotFoundError:
        # print('Operation failed: %s', e.strerror)
        with open(url_country[:3] + 'players_ID.csv', 'w') as file_id, open(url_country[:3] + 'players_Hist.csv',
                                                                            'w') as file_hist:
            csv_hist = csv.writer(file_hist)
            csv_id = csv.writer(file_id)
            csv_hist.writerow(head_hist)
            csv_id.writerow(head_id)
            extractInfo_players(csv_id, csv_hist, url_country[:3], players_list[:])
