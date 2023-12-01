import pymysql

host = '0.0.0.0'
user = 'root'
dbpassword = '7Sanctuaries!'

connection = pymysql.connect(host = host, port = 3307, user = user, password = dbpassword, database = 'air_ticket')
cursor = connection.cursor()

cursor.execute('SELECT booking_agent_id FROM agent')
res = cursor.fetchall()
print(type(res))
print(res)