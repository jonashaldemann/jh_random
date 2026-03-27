import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="dbm0r0wv.mariadb.hosting.zone",
        user="dbm0r0wv_t5j53mg",
        password="s4D5fbz@NhrG",
        database="dbm0r0wv",
        port=3306
    )