import psycopg2
from app.core import config

def establish_connection():
    # Connect to thew db
    try:
        con = psycopg2.connect(
            host = config.HOST,
            database = config.DATABASE,
            user = config.USER,
            password = config.PASSWORD
        )
        # Cursor
        cur = con.cursor()
        return cur, con

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

def db_commit(con):
    con.commit()
    return 0

def close_connection(con, cur):
    # Close the cursor
    cur.close()

    # Close the connection
    con.close()
    return 0

def db_get_all_dogs(cur):
    cur.execute('SELECT * FROM dogs')
    return cur.fetchall()

def db_get_dog_by_name(cur, dog_name):
    cur.execute('SELECT * FROM dogs WHERE name = %s', (dog_name,))
    return cur.fetchall()

def db_get_dog_by_id(cur, dog_id):
    cur.execute('SELECT * FROM dogs WHERE id = %s', (dog_id,))
    return cur.fetchall()

def db_get_adopted_dogs(cur):
    cur.execute('SELECT * FROM dogs WHERE dogs.is_adopted = %s', (True,))
    return cur.fetchall()

def db_insert_dog(cur, name, picture, create_day, update_day, is_adopted, age, weigth):
    cur.execute('INSERT INTO dogs (name, picture, create_day, update_day, is_adopted, age, weigth) \
                VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (name, picture, create_day, update_day, is_adopted, age, weigth))
    return 0

def db_update_dog(cur, name, picture, update_day, is_adopted, age, weigth, dog_id):
    cur.execute('UPDATE dogs \
                SET name = %s, picture = %s, \
                update_day = %s, is_adopted = %s, \
                age = %s, weigth = %s \
                WHERE id = %s', 
                (name, picture, update_day, 
                is_adopted, age, weigth, dog_id)
                )
    return 0

def db_delete_by_id(cur, dog_id):
    cur.execute('DELETE FROM dogs WHERE dogs.id = %s', (dog_id,))
    return 0



