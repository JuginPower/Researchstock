import mysql.connector
from datetime import datetime


class Datamanager:

    def __init__(self):

        self._user = "papi"
        self._hostname = "localhost"
        self._password = "qCMhi0K1L2gjBckYx54n"
        self._database = "stockbase"

    def init_conn(self):

        return mysql.connector.connect(user=self._user, host=self._hostname, password=self._password, database=self._database)

    def select(self, sqlstring):

        mydb = self.init_conn()
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sqlstring)
        result = mycursor.fetchall()
        mydb.close()
        return result

    def query(self, sqlstring, val=None):

        mydb = self.init_conn()
        mycursor = mydb.cursor(buffered=True)

        if isinstance(val, list):
            mycursor.executemany(sqlstring, val)
        elif isinstance(val, tuple):
            mycursor.execute(sqlstring, val)
        elif not val:
            mycursor.execute(sqlstring)

        mydb.commit()
        mydb.close()
        return mycursor.rowcount


new_data = []
dm = Datamanager()
rough_data = dm.select("SELECT * FROM indiz_price")

for item in rough_data:
    new_item = tuple([item[1], item[2], datetime.fromtimestamp(item[-1]).strftime("%Y-%m-%d %H:%M:%S")])
    new_data.append(new_item)

dm.query("TRUNCATE TABLE indiz_price")
dm.query("ALTER TABLE indiz_price MODIFY COLUMN zeit datetime")
inserted_rows = dm.query("INSERT INTO indiz_price (indiz_id, price, zeit) VALUES (%s, %s, %s)", new_data)
print("Rows inserted:", inserted_rows)
