import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events (
                                    staging_event_id int IDENTITY(0,1),
                                    artist varchar,
                                    auth varchar,
                                    firstName varchar,
                                    gender varchar,
                                    itemInSession int,
                                    lastName varchar,
                                    length decimal,
                                    level varchar,
                                    location varchar,
                                    method varchar,
                                    page varchar,
                                    registration decimal,
                                    sessionId int,
                                    song varchar,
                                    status int,
                                    ts bigint,
                                    userAgent varchar,
                                    userId int
                                    )
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs (
                                    artist_id varchar,
                                    artist_latitude decimal,
                                    artist_location varchar,
                                    artist_longitude decimal,
                                    artist_name varchar,
                                    duration decimal,
                                    num_songs int,
                                    song_id varchar PRIMARY KEY,
                                    title varchar,
                                    year int
)
""")

songplay_table_create = ("""
""")

user_table_create = ("""
""")

song_table_create = ("""
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# STAGING TABLES

staging_events_copy = ("""
""").format()

staging_songs_copy = ("""
""").format()

# FINAL TABLES

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
