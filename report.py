import sqlite3
from sqlite3 import Error
import sys


def show_chart_plotly(ids):
    import plotly.express as px
    import pandas as pd

    excel = {}
    for i in ids:
        cur = conn.cursor()
        cur.execute("SELECT name FROM monitor WHERE id=?", (i, ))
        result = cur.fetchone()
        if result == None:
            continue
        else:
            if 'Id' not in excel:
                excel['Id'] = {}
            if 'Name' not in excel:
                excel['Name'] = {}
            if 'Uptime' not in excel:
                excel['Uptime'] = {}
            excel['Id'][i] = i
            excel['Name'][i] = result[0]
            excel['Uptime'][i] = int(percent_by_monitor_id(i))

    data = pd.DataFrame.from_dict(excel)
    fig = px.bar(data, x='Id', y='Uptime', hover_data=['Name'])
    fig.show()


def show_chart_matplotlib(ids):
    import matplotlib.pyplot as plt

    lefts = []
    counter = 1
    percents = {}
    names = {}

    for i in ids:
        cur = conn.cursor()
        cur.execute("SELECT name FROM monitor WHERE id=?", (i, ))
        result = cur.fetchone()
        if result == None:
            continue
        else:
            lefts.append(counter)
            counter += 1
            names[i] = result[0]
            percents[i] = int(percent_by_monitor_id(i))
    
    left = list(lefts)
    height = list(percents.values())
    tick_label = list(lefts)
    
    plt.bar(left, height, tick_label = tick_label, width = 0.8, color = ['green'])
    plt.xlabel('Systems')
    plt.ylabel('UpTime')
    plt.title('HeartBeat')
    plt.show()


def create_connection(kumadb):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(kumadb)
    except Error as e:
        print(e)

    return conn


def count_heartbeat_by_status(monitor_id, status):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM heartbeat WHERE monitor_id=? AND status=?", (monitor_id, status))
    result = cur.fetchone()

    return result[0]


def percent_by_monitor_id(monitor_id):
    rows = count_heartbeat_by_monitor_id(monitor_id)
    result = count_heartbeat_by_status(monitor_id, 1)

    if rows == 0:
        return 0

    percentage = (result / rows) * 100
    return percentage


def count_heartbeat_by_monitor_id(monitor_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM heartbeat WHERE monitor_id=?", (monitor_id,))

    rows = cur.fetchone()

    return rows[0]
 

def main(args):
    global conn

    if len(args) != 2:
        print('Usage: python report.py UPTIME_KUMA_DATABASE_FILE')
        exit(1)

    DATABASE = args[1]

    # create a database connection
    conn = create_connection(DATABASE)
    with conn:
        show_chart_plotly([1, 3, 10]) # list of IDs of monitors to report

        
if __name__ == '__main__':
    main(sys.argv)