import psycopg2


conn = psycopg2.connect(database="WMS_BOT",
                        host="127.0.0.1",
                        user="root",
                        password="z7uBF5vwCRKf"
)
cursor = conn.cursor()

cur.execute("CREATE TABLE your_table_name (login VARCHAR(255), uid INTEGER PRIMARY KEY);")
conn.commit()
cur.close()
conn.close()
