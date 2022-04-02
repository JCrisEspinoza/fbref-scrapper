# coding: utf-8

import os.path
from pathlib import Path

import pandas as pd
import numpy as np
import csv 

BASE_DIR = Path(__file__).resolve().parent

def extractPerfPlayer(playerInterHist,href):
    # playerInterHist : DataFrame
    # href            : url player
        
    s = href.split('/')
    href = '/'.join((s[2],s[3],s[4],s[5],'dom_lg',s[6]+'-Domestic-League-Stats'))
    print('http://fbref.com' + href)
    tables = pd.read_html('http://fbref.com' + href)
            
    #print('tablas',len(tables))
    dat = playerInterHist[['ID','Season','Squad']]
    #print(playerInterHist.set_index('ID').to_dict())    
    print(dat)
    print('----------------------------------')
    for table in tables[:-2]:                   #getout 2 last html tables
        list=[]
        [list.append(column[1]) for column in table.columns]
        table.columns = list            
        f_sea = table['Season'].isin(playerInterHist['Season'])
        f_sqd = table['Squad'].isin(playerInterHist['Squad'])
        tab = table[f_sea & f_sqd].iloc[:,6:-1]
        #print(tab)
        if dat.shape[1] == 3:
            dat = pd.concat([table[f_sea & f_sqd].iloc[:,0],tab],axis=1)
        else:
            dat=pd.concat([dat,tab],axis=1)
        #print(dat)
    
    output = pd.merge(playerInterHist[['ID','Season','Squad']],dat,on='Season')    
    return output.values.tolist()

def extract_PerfPlayers(csv,playersID,playerHist):
        
    # csv       : file object
    # playersID : dataframe
    # playersHist: dataframe
    
    for ID,href in zip(playersID.ID,playersID.player_page):
        #print(players_hist.loc[players_hist['ID'] == ID])
        playerInter = checkInter(playerHist[playerHist['ID'] == ID])
        
        if len(playerInter.Season): 
            print(href)           
            #data= extractPerfPlayer(seasons.to_list(),'http://' + href)
            #print(data.shape)            
            rows = extractPerfPlayer(playerInter,'http://' + href)         
            csv.writerows(rows)
        else: 
            pass
        
def checkInter(playerHist):
    country_out = ['ESP', 'ITA', 'FRA','ENG','GER', 'USA']

    bool_value = playerHist['country'].isin(country_out)                  # boolean column['country] of dataframe
    player_check = playerHist.loc[lambda playerHist: bool_value == 1, :]  # rows where match countr_out rows-year = rows.year 
       
    return player_check   


if __name__ == '__main__':
    
    dist_folder = os.path.join(BASE_DIR, 'dist')
    H = open('head_perf.txt', 'r')
    head = H.read().split('\n') 
  
    for country in os.listdir(dist_folder):
        
        country_folder = os.path.join(dist_folder, country)   
        player_file = os.path.join(country_folder, f'{country}.players.csv')
        player_info_file = os.path.join(country_folder, f'{country}.hist.csv')
        player_perf = os.path.join(country_folder, f'{country}.perf.csv')

        players_id = pd.read_csv(player_file)
        players_hist = pd.read_csv(player_info_file) 

        if os.path.exists(player_perf):
            f = open(player_perf, 'a+', encoding='utf-8')
            player_csv = csv.writer(f)
            #open_files.append(f)            # pendiente ultimo registro
        else:
            f = open(player_perf, 'w', encoding='utf-8')
            player_csv = csv.writer(f)
            player_csv.writerow(head)
            #open_files.append(f)
       
        extract_PerfPlayers(player_csv,players_id,players_hist)
        f.close()






