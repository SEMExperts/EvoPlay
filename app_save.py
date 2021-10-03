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
    id_dict = database.city_id('2020-01-01', '2020-11-02')

    # Get cities list
    cities = list(id_dict.keys())

    # Get color list
    colors = [
        "#F7604D",
        "#4ED6B8",
        "#A8D582",
        "#D7D768",
        "#9D66CC",
        "#DB9C3F",
        "#3889FC"
    ]

    # Get cities values list
    city_values = []
    for id in id_dict:
        city_value = database.city_lookup_value(id_dict[id])
        city_values.append(city_value)

    # Get tuple for pie_chart template
    pie_chart_data = tuple(zip(cities, city_values, colors[:len(city_values)]))

    # Get tuple for cumsums template
    cumsum_list = []
    id_color = 0
    for id in id_dict:
        dict = database.month_lookup_value(id_dict[id])
        monthes = list(dict.keys())
        values = list(dict.values())
        cumsum = np.cumsum(np.array(values))
        tuple = (id, cumsum, colors[id_color])
        id_color += 1
        cumsum_list.append(tuple)

    return render_template('index.html',
                           pie_chart_data=pie_chart_data,
                           cumsum_list=cumsum_list,
                           monthes=monthes)


@app.route('/plt/')
def pie_chart():
    id_dict = database.city_id('2020-01-01', '2020-11-02')

    # Get cities list
    cities = list(id_dict.keys())

    # Get color list
    colors = [
        "#F7604D",
        "#4ED6B8",
        "#A8D582",
        "#D7D768",
        "#9D66CC",
        "#DB9C3F",
        "#3889FC"
    ]

    # Get cities values list
    city_values = []
    for id in id_dict:
        city_value = database.city_lookup_value(id_dict[id])
        city_values.append(city_value)

    # Get tuple for pie_chart template
    pie_chart_data = tuple(zip(cities, city_values, colors[:len(city_values)]))

    return render_template('index.html', pie_chart_data=pie_chart_data)

@app.route('/month/')
def month():
    id_dict = database.city_id('2020-07-01', '2020-11-28')

    colors = [
        "#F7604D",
        "#4ED6B8",
        "#A8D582",
        "#D7D768",
        "#9D66CC",
        "#DB9C3F",
        "#3889FC"
    ]

    # Get cumsums for cities
    cumsum_list = []
    id_color = 0
    for id in id_dict:
        dict = database.month_lookup_value(id_dict[id])
        monthes = list(dict.keys())
        values = list(dict.values())
        cumsum = np.cumsum(np.array(values))
        tuple = (id, cumsum, colors[id_color])
        id_color += 1
        cumsum_list.append(tuple)

    return render_template('index.html', cumsum_list=cumsum_list, monthes=monthes)


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


if __name__ == '__main__':
    app.run()
