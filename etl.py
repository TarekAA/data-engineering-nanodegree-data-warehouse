import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """Execute COPY commands to load data from S3 Bucket into staging area.
    The COPY sql commands are present in `sql_queries`.
    This copies log data into the following tables:

    - staging_events
    - staging_songs

    :param cur: Cursor object. Allows python code to execute PostgreSQL in a database session
    :param conn: Connection to the data warehouse. It encapsulate the database session
    :return: None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """Execute all insert queries as present in `sql_queries`.
    This inserts data from staging area into the following tables:

    - songplay
    - user
    - song
    - artist
    - time

    :param cur: Cursor object. Allows python code to execute PostgreSQL in a database session
    :param conn: Connection to the data warehouse. It encapsulate the database session
    :return: None
    """
    for query in insert_table_queries:
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

    # load data from s3 buckets into staging area
    load_staging_tables(cur, conn)
    # move data from staging area into final models
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
