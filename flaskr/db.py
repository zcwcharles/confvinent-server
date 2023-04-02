from flask_mysqldb import MySQL

db = MySQL()

def parse_select_result(cursor):
  column_names = [el[0] for el in cursor.description]
  data = cursor.fetchall()
  n = len(column_names)
  res = []

  for entry in data:
    obj = {}
    for i in range(n):
      obj[column_names[i]] = entry[i]
    res.append(obj)

  cursor.close()
  
  return res

def execute_select_query(query):
  cursor = db.connection.cursor()
  cursor.execute(query)
  return parse_select_result(cursor)

def execute_modify_query(query):
  cursor = db.connection.cursor()
  cursor.execute(query)
  db.connection.commit()
  cursor.close()
