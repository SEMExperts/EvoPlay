import sqlite3


class SQLite:

    def __init__(self, db_name='history.db'):
        self.db = db_name

    def create(self):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS data(
            dates DATE,
            country TEXT,
            target REAL
            )
                ''')
        conn.commit()
        conn.close()

    # Add Many Records To Table
    def add_many(self, list):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.executemany("INSERT INTO data VALUES (?,?,?)", (list))
        conn.commit()
        conn.close()

    # Get all cities (without Nan) and they id
    def city_id(self, from_date='2020-01-01', to_date='2020-12-28'):
        from collections import defaultdict

        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM data WHERE dates >= (?) AND dates <= (?) AND country != 'nan' ORDER BY dates",
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

        return city_id_dict

    def city_lookup_value(self, list_id):
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        args = list_id
        query = f'''SELECT SUM(target)
                FROM data 
                WHERE rowid IN ({','.join(['?'] * len(args))})'''
        c.execute(query, args)
        items = c.fetchall()
        for item in items[0]:
            value = item

        return value

    # Get cities and they gross value from date to dare
    def month_lookup_value(self, list_id):
        month = []
        value = []
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        args = list_id
        query = f'''SELECT SUM(target), strftime('%m',dates) AS month, strftime('%Y',dates) AS year
        FROM data 
        WHERE rowid IN ({','.join(['?'] * len(args))})
        GROUP BY month 
        ORDER BY dates'''
        c.execute(query, args)
        items = c.fetchall()

        for item in items:
            month.append(item[1])
            value.append(item[0])

        dict = {}

        for i in range(len(month)):
            dict[month[i]] = value[i]

        return dict












