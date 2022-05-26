import sqlite3
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from itertools import combinations


def radarplot(df, nac1, nac2, pw):
    dg = df.groupby('nac')
    dg1 = dg.agg(np.mean).loc[nac1].reset_index()
    dg2 = dg.agg(np.mean).loc[nac2].reset_index()

    dg1.columns = ['variables', 'mean']
    dg2.columns = ['variables', 'mean']

    dg1 = pd.concat([dg1, pd.DataFrame(len(variables) * [nac1], columns=['nac'])], axis=1)
    dg2 = pd.concat([dg2, pd.DataFrame(len(variables) * [nac2], columns=['nac'])], axis=1)

    df = pd.concat([dg1, dg2])
    df['mean'] = (df['mean'] - df['mean'].min()) / (df['mean'].max() - df['mean'].min())
    df = df.dropna()

    var = dg1.dropna().variables
    var = [*var, var[0]]

    values_1 = df[df['nac'] == nac1]['mean']
    values_2 = df[df['nac'] == nac2]['mean']

    values_1 = [*values_1, values_1[0]]
    values_2 = [*values_2, values_2[0]]

    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(values_1))

    plt.figure(figsize=(8, 8))
    plt.subplot(polar=True)
    plt.plot(label_loc, values_1, label=nac1)
    plt.plot(label_loc, values_2, label=nac2)

    for i in range(len(pw)):
        if pw.loc[pw.index[i], 'plegend'] == 1:
            plt.text(label_loc[i], values_1[i], '**', )
    plt.title('Teams profiles', size=20, y=1.05)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=var)
    plt.legend()

    return plt


def diferenceAnalytic(df, nac1, nac2):
    nacs = df.groupby('nac').nunique().index
    dA = pd.DataFrame(columns=[nac1 + "-" + nac2], index=df.columns[:-1])
    p_warning = pd.DataFrame(columns=['plegend'], index=df.columns[:-1])
    for variable in dA.index:
        dA.loc[variable, nac1 + "-" + nac2] = stats.ttest_ind(df.groupby('nac').get_group(nac1)[variable],
                                                              df.groupby('nac').get_group(nac2)[variable]
                                                              )[1]  # p-valor
        if stats.ttest_ind(df.groupby('nac').get_group(nac1)[variable], df.groupby('nac').get_group(nac2)[variable])[
            1] < .05:
            p_warning.loc[variable, 'plegend'] = 1
        else:
            p_warning.loc[variable, 'plegend'] = 0

    return dA, p_warning


def descriptive(df):
    dp = pd.DataFrame(columns=dTS.columns[:-1])
    dg = df.groupby('nac')
    dm = dg.agg(np.mean)
    ds = dg.agg(np.std)
    for i in dm.index:
        for j in dm.columns:
            dp.loc[i, j] = str("{:.2f}".format(dm.loc[i, j])) + ' +/- ' + str("{:.2f}".format(ds.loc[i, j]))

    return dp


if __name__ == '__main__':

    conn = sqlite3.connect(os.environ.get("DB_PATH"))
    print('Connected to database successfully.')
    players = pd.read_sql_query("SELECT * from user", conn)
    basic_stats = pd.read_sql_query("SELECT * from basic_stats", conn)

    countries = ['arg', 'bra']  # ,'col','chi','ecu','uru']
    seasons = ['2016-2017', '2017-2018']  # ,'2018-2019','2019-2020','2020-2021','2021-2022']
    levels = ['1. La Liga', '1. Ligue 1', '1. Premier League', '1. Serie A', '1. Bundesliga']
    dm = pd.DataFrame([['time_stats', 5, 10, 'ts'],  # Influence 13,18
                       ['shooting_stats', 3, 14, 'ss'],  # DO
                       ['possession_stats', 3, 26, 'ps'],  # DO
                       ['gca_stats', 3, 18, 'gca'],  # DO goals and shoot creations
                       ['defense_stats', 3, 7, 'ds1'],  # DD takles
                       ['defense_stats', 8, 11, 'ds2'],  # DD takles vs dribb
                       ['defense_stats', 12, 17, 'ds3'],  # DD press
                       ['defense_stats', 18, 21, 'ds4'],  # DD blk
                       # ['defense_stats',           ],     #miscelaneus
                       # ['passing_pass_stats',      ],   #takles
                       ], columns=['stats', 'var_i', 'var_k', 'key_stat']
                      )

    for metric_i in range(1, 2):

        for level in levels:
            dCount = pd.DataFrame(columns=seasons, index=countries)
            for season in seasons:

                print("*****************************************************************")
                print("Se analizarán las métricas de: " + dm.iloc[int(metric_i) - 1, 0])
                print("de la temporada: " + season)
                print("de la liga: " + level)
                # print("SELECT * from "+ metrics[int(metric_i)-1])
                print("*****************************************************************")
                TS_raw = pd.read_sql_query("SELECT * from " + dm.iloc[int(metric_i) - 1, 0], conn)

                low = dm.iloc[int(metric_i) - 1, 1]
                top = dm.iloc[int(metric_i) - 1, 2]

                dTS = pd.DataFrame(
                    columns=TS_raw.columns[low:top].values)
                dTS.insert(len(dTS.columns), 'nac', True)

                variables = dTS.columns
                for ctry in countries:
                    print(ctry)
                    players_id = players[players.country == ctry].id

                    BS1 = basic_stats[basic_stats.user_id.isin(players_id)]
                    BS2 = BS1[BS1.comp_level == level]
                    BS3 = BS2[BS2.season == season]

                    TS_ = TS_raw[TS_raw.id.isin(BS3.id)]
                    TS_ = TS_[TS_.season == season]
                    TS_.insert(len(TS_.columns), 'nac', len(TS_) * [ctry], True)

                    dTS = pd.concat([dTS, TS_[variables]])
                    dTS = dTS.dropna(how='any')  # clean nan data

                # Se define el nombre de la carpeta o directorio a crear

                path = os.environ.get("RESULT_PATH")
                dir_ = os.path.join(path, level[3:] + "/" + season)
                if not os.path.isdir(dir_):
                    os.makedirs(dir_)
                    print('Se ha creado el directorio.')
                else:
                    print('El directorio ya existe.')

                # ---------   Statistic Analysis ------------------

                if len(dTS) > 1:
                    dTS.iloc[:, :-1] = dTS.iloc[:, :-1].astype(float)
                    stat = dm.iloc[int(metric_i) - 1, 3]

                    dp = descriptive(dTS)  # tabla descriptiva (mean +/- std)de resultados
                    dp.to_excel(dir_ + "/" + stat + "descriptive.xlsx")  # guardar

                    for var in dTS.columns[:-1]:  # boxplot por variable
                        print(var)
                        dTS.plot(kind='box', column=var, by='nac', grid=False, title=season, fontsize=18)  #

                        plt.savefig(dir_ + "/" + stat + "_" + var + "_boxplot.png")
                        plt.close()

                    d_analytic = pd.DataFrame(index=dTS.columns[:-1])
                    for nac in list(
                            combinations(dTS.groupby('nac').nunique().index, 2)):  # tablas p-value nac0 vs nac1
                        dA = diferenceAnalytic(dTS, nac[0], nac[1])
                        d_analytic = pd.concat([d_analytic, dA[0]], axis=1)  # faltan size efect o IC
                        plt = radarplot(dTS, nac[0], nac[1], dA[1])  # radarplot nac0 vs nac1
                        plt.savefig(dir_ + "/" + stat + "_" + nac[0] + "-" + nac[1] + "_radplot.png")
                        plt.close()
                    d_analytic.to_excel(dir_ + "/" + stat + '_inferencial_results.xlsx')

            dCount.to_excel(dir_ + 'count.xlsx')
    conn.close()
