
import os
import time

from urllib.request import urlopen

import psycopg2.extras

import conf


def save_img(category_id, img):
    resource = urlopen(img)
    out = open("data/train/{}/{}.jpg".format(category_id, os.urandom(8).hex()), 'wb')
    out.write(resource.read())
    out.close()


db_connection = psycopg2.connect(
    host=conf.host, port=conf.port,
    database=conf.database,
    user=conf.user,
    password=conf.password,
    cursor_factory=psycopg2.extras.DictCursor
)

# споты и трек системы 487
# потолочные светильники 481
# настольные лампы 482

category_ids = (487, 481, 482)

for category_id in category_ids:
    cursor = db_connection.cursor()
    cursor.execute("select * from product.product where category_id = %s and picture_url != '' limit 2000",
                   (category_id,))

    products = cursor.fetchall()

    for product in products:
        time.sleep(1)

        picture_url = product.get('picture_url')
        try:
            save_img(category_id, picture_url)
        except:
            pass
