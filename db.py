from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] =''
app.config['MYSQL_DATABASE_DB'] = 'binarybits'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()
# email="aryanpatel19aug3@gmail.com"
# cursor.execute("select * from faculty where email=(%s),(email)")
# result = cursor.fetchone()
# print(result)
# cursor.execute("SELECT * from user")
# data = cursor.fetchone()
# print(data)