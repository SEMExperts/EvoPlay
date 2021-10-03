from flask import Flask, render_template, request, jsonify
# import database
import numpy as np
from database import SQLite
import pandas as pd

app = Flask(__name__)
db = SQLite()


@app.route('/')
def home():
    id_dict = db.city_id('2020-01-01', '2020-12-28')

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
        city_value = db.city_lookup_value(id_dict[id])
        city_values.append(city_value)

    # Get cumsums for cities
    cumsum_list = []
    id_color = 0
    for id in id_dict:
        dict = db.month_lookup_value(id_dict[id])
        monthes = list(dict.keys())
        values = list(dict.values())
        cumsum = np.cumsum(np.array(values))
        tuple = (id, cumsum, colors[id_color])
        id_color += 1
        cumsum_list.append(tuple)

    return render_template('index.html',
                           cities=cities,
                           pie_values=city_values,
                           pie_colors=colors[:len(city_values)],
                           cumsum_list=cumsum_list,
                           monthes=monthes,
                           colors=colors)

@app.route('/new/', methods=["POST","GET"])
def new():
    if request.method == 'POST':
        From = request.form.get("From")
        to = request.form.get("to")
        id_dict = db.city_id(From, to)

    else:
        id_dict = db.city_id('2020-01-01', '2020-12-28')

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
        city_value = db.city_lookup_value(id_dict[id])
        city_values.append(city_value)

    # Get cumsums for cities
    cumsum_list = []
    id_color = 0
    for id in id_dict:
        dict = db.month_lookup_value(id_dict[id])
        monthes = list(dict.keys())
        values = list(dict.values())
        cumsum = np.cumsum(np.array(values))
        tuple = (id, cumsum, colors[id_color])
        id_color += 1
        cumsum_list.append(tuple)

    return render_template('index_no_js.html',
                           cities=cities,
                           pie_values=city_values,
                           pie_colors=colors[:len(city_values)],
                           cumsum_list=cumsum_list,
                           monthes=monthes,
                           colors=colors)


@app.route('/csv/')
def csv_to_database():
    db.create()
    df = pd.read_csv('test_dataset.csv', delimiter=',')
    list_of_rows = [list(row) for row in df.values]

    db.add_many(list_of_rows)

    return 'DataBase created'

@app.route("/range",methods=["POST","GET"])
def range():
    if request.method == 'POST':
        From = request.form['From']
        to = request.form['to']
        print(From)
        print(to)
        id_dict = db.city_id(From, to)
        # Get cities list

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
            city_value = db.city_lookup_value(id_dict[id])
            city_values.append(city_value)

        # Get cumsums for cities
        cumsum_list = []
        id_color = 0
        for id in id_dict:
            dict = db.month_lookup_value(id_dict[id])
            monthes = list(dict.keys())
            values = list(dict.values())
            cumsum = np.cumsum(np.array(values))
            tuple = (id, cumsum, colors[id_color])
            id_color += 1
            cumsum_list.append(tuple)
    return jsonify({'htmlresponse': render_template('response.html',
                                                    cities=cities,
                                                    pie_values=city_values,
                                                    pie_colors=colors[:len(city_values)],
                                                    cumsum_list=cumsum_list,
                                                    monthes=monthes,
                                                    colors=colors)})


if __name__ == '__main__':
    app.run()
