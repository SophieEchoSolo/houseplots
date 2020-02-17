import pymysql.cursors
import matplotlib.pylab as plt
import numpy as np
from itertools import zip_longest

# Connect to the database
connection = pymysql.connect(host='localhost',
							 user='root',
							 password='',
							 db='housing',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)

def _label_barh(ax, bars, text_format, **kwargs):
    """
    Attach a text label to each bar displaying its y value
    Note: label always outside. otherwise it's too hard to control as numbers can be very long
    """
    max_x_value = ax.get_xlim()[1]
    distance = max_x_value * 0.0025

    for bar in bars:
        text = text_format.format(bar.get_width())

        text_x = bar.get_width() + distance
        text_y = bar.get_y() + bar.get_height() / 2

        ax.text(text_x, text_y, text, va='center', **kwargs)

def hbar_chart(sql, file_name, plot_title):
    vals = ()
    x_vals = []
    y_vals = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        for index in range(len(result)):
            x = result[index]["label"]
            y = float(result[index]["value"])
            x_vals.append(x)
            y_vals.append(y)
        vals = zip(x_vals, y_vals)
       
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(x_vals))

    bars = ax.barh(y_pos, y_vals, align = "center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(x_vals)
    ax.set_xlabel('Average Rent (SEK)')
    ax.set_title(plot_title)

    _label_barh(ax, bars, "{:.6}")
       
    plt.show()
    plt.savefig(file_name)


hbar_chart(sql = """SELECT region AS label, AVG(rent) AS value FROM houses GROUP BY region ORDER BY value DESC;""", file_name = "rent-per-region.png", plot_title = "Avg Rent By Region")