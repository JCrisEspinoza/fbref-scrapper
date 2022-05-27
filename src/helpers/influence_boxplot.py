from PIL import Image
import matplotlib.pyplot as plt
import os

seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
levels = ['1. La Liga', '1. Ligue 1', '1. Premier League', '1. Serie A', '1. Bundesliga']

w = 10
h = 10
fig = plt.figure(figsize=(10, 15))
columns = 2
rows = 5

for level in levels:
    i = 1
    for season in seasons:

        path = os.environ.get("RESULT_PATH")
        dir_ = os.path.join(path, level[3:] + "/" + season)
        if not os.path.isdir(dir_):
            os.makedirs(dir_)
            print('Se ha creado el directorio %s.' % dir_)
        else:
            print('El directorio %s ya existe.' % dir_)

        img1 = Image.open(dir_ + "/" + "ts_points_per_match_boxplot.png")
        img3 = Image.open(dir_ + "/" + "ts_plus_minus_per90_boxplot.png")

        fig.add_subplot(rows, columns, i)
        # ig.size =
        plt.axis('off')
        plt.imshow(img1)
        i = i + 1

        fig.add_subplot(rows, columns, i)
        plt.axis('off')
        plt.imshow(img3)
        i = i + 1

    plt.tight_layout(pad=.9, w_pad=0.9, h_pad=1.0)
    plt.savefig(level + "_influence_boxplots.png")
    plt.close()
