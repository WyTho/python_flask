import mysql.connector as mariadb


def clear_database():
    mariadb_connection = mariadb.connect(user='dev', password='secret', database='test_env')
    cursor = mariadb_connection.cursor()

    cursor.execute("DELETE FROM _hour;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _day;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _event_call;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _event;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _usage;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _item_group;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _item")
    cursor.execute("ALTER TABLE _item AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _group;")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _graph;")
    mariadb_connection.commit()

    print('DATABASE CLEARED')
