from flask import Flask, render_template, send_file
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import database
import matplotlib.pyplot as plt
import numpy as np



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plt/')
def pie_chart():
    id_dict = database.city_id('2020-01-01', '2020-11-02')
    values = []
    for id in id_dict:
        value = database.city_lookup_value(id_dict[id])
        values.append(value)

    cities = list(id_dict.keys())

    plt.pie(values, labels=cities, autopct='%2.1f%%')
    plt.show()

    return render_template('test.html')

@app.route('/month/')
def month():
    id_dict = database.city_id('2020-01-01', '2020-11-28')

    for id in id_dict:
        dict = database.month_lookup_value(id_dict[id])

        monthes = list(dict.keys())
        values = list(dict.values())
        cumsum = np.cumsum(np.array(values))

        xpoints = monthes
        ypoints = cumsum

        plt.plot(xpoints, ypoints)
        plt.suptitle(f'{id}\n\n', fontweight="bold")
        plt.scatter(xpoints, ypoints, color='blue', s=50, marker='o')
        plt.gcf().autofmt_xdate()

        plt.show()

    return render_template('test.html')


@app.route('/csv/')
def csv_to_database():
    import sqlite3

    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data(
    dates DATE,
    country TEXT,
    target REAL
    )
        ''')
    conn.commit()
    conn.close()

    import pandas as pd
    df = pd.read_csv('test_dataset.csv', delimiter=',')
    list_of_rows = [list(row) for row in df.values]
    database.add_many(list_of_rows)

    return 'Downloading csv'

@app.route('/visualize')
def visualize():

    id_dict = database.city_id('2020-01-01', '2020-11-28')

    for id in id_dict:
        dict = database.month_lookup_value(id_dict[id])

        monthes = list(dict.keys())
        values = list(dict.values())
        cumsum = np.cumsum(np.array(values))

        xpoints = monthes
        ypoints = cumsum

    x = xpoints
    y = ypoints
    fig, ax = plt.subplots(figsize=(5, 5))
    ax = sns.set_style(style='darkgrid')
    sns.lineplot(x, y)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='img/png')





if __name__ == '__main__':
    app.run()
