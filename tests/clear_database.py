import mysql.connector as mariadb


def clear_database():
    mariadb_connection = mariadb.connect(user='dev', password='secret', database='test_env')
    cursor = mariadb_connection.cursor()

    cursor.execute("DELETE FROM _preset_action;")
    cursor.execute("ALTER TABLE _preset_action AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _preset;")
    cursor.execute("ALTER TABLE _preset AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _schedule_day;")
    cursor.execute("ALTER TABLE _schedule_day AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _scheduled_usage;")
    cursor.execute("ALTER TABLE _scheduled_usage AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _schedule;")
    cursor.execute("ALTER TABLE _schedule AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _hour;")
    cursor.execute("ALTER TABLE _hour AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _day;")
    cursor.execute("ALTER TABLE _day AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _event_call;")
    cursor.execute("ALTER TABLE _event_call AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _event;")
    cursor.execute("ALTER TABLE _event AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _usage;")
    cursor.execute("ALTER TABLE _usage AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _item_group;")
    cursor.execute("ALTER TABLE _item_group AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _item")
    cursor.execute("ALTER TABLE _item AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _group;")
    cursor.execute("ALTER TABLE _group AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    cursor.execute("DELETE FROM _graph;")
    cursor.execute("ALTER TABLE _graph AUTO_INCREMENT = 1")
    mariadb_connection.commit()

    print('DATABASE CLEARED')
