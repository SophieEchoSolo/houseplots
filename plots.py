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

def hbar_chart(sql, file_name):
    vals = ()
    x_vals = []
    y_vals = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        for index in range(len(result)):
            x = result[index]["label"]
            y = result[index]["value"]
            x_vals.append(x)
            y_vals.append(y)
        vals = zip(x_vals, y_vals)
    
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(x_vals))

    ax.barh(y_pos, y_vals, align = "center")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(x_vals)
    ax.set_xlabel('Average Rent')
    
    plt.show()
    plt.savefig(file_name)

hbar_chart(sql = """SELECT region AS label, ROUND(AVG(rent)) AS value FROM houses GROUP BY region ORDER BY value DESC;""", file_name = "test3.png")