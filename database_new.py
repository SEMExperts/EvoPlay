import sqlite3


# Query The DB and Return All Records
def show_all():
    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM data")
    items = c.fetchall()

    for item in items:
        print(item)

    conn.commit()
    conn.close()


# Add Many Records To Table
def add_many(list):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.executemany("INSERT INTO data VALUES (?,?,?)", (list))
    conn.commit()
    conn.close()


# Get all cities (without Nan) and they id
def city_id(from_date, to_date):
    from collections import defaultdict

    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * from data WHERE dates >= (?) and dates <= (?) and country != 'nan' ORDER BY dates",
              (from_date, to_date))
    items = c.fetchall()
    city = []
    rowid = []

    for item in items:
        city.append(item[2])
        rowid.append(item[0])

    city_id = zip(city, rowid)

    city_id_dict = defaultdict(list)
    for city, rowid in city_id:
        city_id_dict[city].append(rowid)

    conn.commit()
    conn.close()

    return city_id_dict

def dates_lookup(list_id):
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    args = list_id
    query = f'''SELECT SUM(target)
            FROM data 
            WHERE rowid in ({','.join(['?'] * len(args))})'''
    c.execute(query, args)
    item = c.fetchall()
    for item in item:
        value = item[0]

    conn.commit()
    conn.close()

    return value


# Get months and gross values from list id
def id_lookup_daily(list_id):
    date = []
    value = []

    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    args = list_id
    query = f'''SELECT SUM(target), strftime('%d',dates) as date, strftime('%Y',dates) as year
        FROM data 
        WHERE rowid in ({','.join(['?'] * len(args))})
        GROUP BY date 
        ORDER BY dates'''
    c.execute(query, args)
    items = c.fetchall()

    for item in items:
        date.append(item[1])
        value.append(item[0])
    conn.commit()
    conn.close()

    dict = {}

    for i in range(len(date)):
        dict[date[i]] = value[i]

    return dict


# Get cities and they gross value from date to dare
def dates_lookup_month(list_id):
    month = []
    value = []
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    args = list_id
    query = f'''SELECT SUM(target), strftime('%m',dates) as month, strftime('%Y',dates) as year
    FROM data 
    WHERE rowid in ({','.join(['?']*len(args))})
    GROUP BY month 
    ORDER BY dates'''
    c.execute(query, args)
    items = c.fetchall()

    for item in items:
        month.append(item[1])
        value.append(item[0])
    conn.commit()
    conn.close()

    dict = {}

    for i in range(len(month)):
        dict[month[i]] = value[i]

    return dict










