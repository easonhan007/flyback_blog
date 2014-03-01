from pymongo import Connection

conn = Connection()
db = conn.test 
db.drop_collection('users')

admin = {'name': 'root', 'password': 'root', 'role': 'admin'}
db.users.insert(admin)

