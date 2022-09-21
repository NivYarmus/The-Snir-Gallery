import sqlite3
from database.queries import *
from Crypto.Hash import SHA256


username = 'Nivyar'
password = 'Nivyar'

username_sha = SHA256.new()
password_sha = SHA256.new()


conn = sqlite3.connect('./project/database/gallery.db')
curr = conn.cursor()


curr.execute(CREATE_ADMINS_TABLE_QUERY)

username_sha.update(username.encode())
password_sha.update(password.encode())

curr.execute(ADD_ADMIN_QUERY, (username_sha.hexdigest(), password_sha.hexdigest()))


conn.commit()

conn.close()