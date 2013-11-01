import bottle
from bottle import route, run
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
db = os.environ["HEROKU_POSTGRESQL_PURPLE_URL"]
url = urlparse.urlparse(db)

@route('/increment_number_of_rages')
def increment_rages():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from t1 WHERE id=1;")
    number_of_rages = cur.fetchone()[2] + 1
    cur.execute("UPDATE t1 SET num=(%s) WHERE id=1;", 
        (number_of_rages,))
    cur.close()
    conn.commit()
    conn.close()

@route('/increment_number_of_tranq')
def increment_tranq():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from t1 WHERE id=2;")
    number_of_rages = cur.fetchone()[2] + 1
    cur.execute("UPDATE t1 SET num=(%s) WHERE id=2;", 
        (number_of_rages,))
    cur.close()
    conn.commit()
    conn.close()

@route('/decrement_number_of_rages')
def decrement_rages():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from t1 WHERE id=1;")
    number_of_rages = cur.fetchone()[2] - 1
    cur.execute("UPDATE t1 SET num=(%s) WHERE id=1;", 
        (number_of_rages,))
    cur.close()
    conn.commit()
    conn.close()

@route('/decrement_number_of_tranq')
def decrement_tranq():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from t1 WHERE id=2;")
    number_of_rages = cur.fetchone()[2] - 1
    cur.execute("UPDATE t1 SET num=(%s) WHERE id=2;", 
        (number_of_rages,))
    cur.close()
    conn.commit()
    conn.close()

@route('/get_number_of_tranq')
def get_tranq():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from t1 WHERE id=2;")
    number_of_tranq = cur.fetchone()
    cur.close()
    conn.close()
    return str(number_of_tranq[2])

@route('/get_number_of_rages')
def get_rages():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from t1 WHERE id=1;")
    number_of_rages = cur.fetchone()
    cur.close()
    conn.close()
    return str(number_of_rages[2])

if __name__ == "__main__":
    run(host='localhost', port=8080)

app = bottle.default_app()