import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """Execute all drop table queries as present in `sql_queries`.
    This drops the following tables if they exists:

    - staging_events
    - staging_songs
    - songplay
    - user
    - song
    - artist
    - time

    :param cur: Cursor object. Allows python code to execute PostgreSQL in a database session
    :param conn: Connection to the data warehouse. It encapsulate the database session
    :return: None
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """Execute all drop table queries as present in `sql_queries`.
    This creates the following tables:

    - staging_events
    - staging_songs
    - songplay
    - user
    - song
    - artist
    - time

    :param cur: Cursor object. Allows python code to execute PostgreSQL in a database session
    :param conn: Connection to the data warehouse. It encapsulate the database session
    :return: None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    # obtain a configuration object
    config = configparser.ConfigParser()
    # parse configuration file `dwh.cfg`
    config.read('dwh.cfg')

    # obtain a database session through connection object
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    # obtain cursor object to execute queries
    cur = conn.cursor()

    # drop all tables if they exits
    drop_tables(cur, conn)
    # create all models schema
    create_tables(cur, conn)

    # close database session
    conn.close()


if __name__ == "__main__":
    main()
