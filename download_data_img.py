
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

category_ids = (487,)

for category_id in category_ids:
    cursor = db_connection.cursor()
    cursor.execute("""select id, picture_url from product.product where category_id = %s and picture_url != ''
                      order by id desc""",
                   (category_id,))

    products = cursor.fetchall()

    count_url = 0
    saved_img = 0

    for product in products:
        if saved_img != 2000:
            time.sleep(0.2)

            picture_url = product.get('picture_url')
            count_url = count_url + 1
            try:
                print(count_url)
                print('saving {} category -- {}'.format(category_id, picture_url))
                save_img(category_id, picture_url)
                saved_img = saved_img + 1
                print('saved')

            except:
                pass
        else:
            break
