
import os

from urllib.request import urlopen
import psycopg2.extras

import conf


def save_img(img):
    resource = urlopen(img)
    out = open("data/train/{}.jpg".format(os.urandom(8).hex()), 'wb')
    out.write(resource.read())
    out.close()


db_connection = psycopg2.connect(
    host=conf.host, port=conf.port,
    database=conf.database,
    user=conf.user,
    password=conf.password,
    cursor_factory=psycopg2.extras.DictCursor
)

cursor = db_connection.cursor()
cursor.execute('select * from shop.shop limit 1')

a = cursor.fetchone()
print(a)
