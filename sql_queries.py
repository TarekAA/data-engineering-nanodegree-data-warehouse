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

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                            artist_id varchar PRIMARY KEY,
                            name varchar,
                            location varchar,
                            latitude decimal,
                            longitude decimal
                            )
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (
                            start_time bigint PRIMARY KEY,
                            hour int,
                            day int,
                            week int,
                            month int,
                            year int,
                            weekday int
                            )
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                            user_id int PRIMARY KEY,
                            first_name varchar,
                            last_name varchar,
                            gender varchar,
                            level varchar
                            )
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                            song_id varchar PRIMARY KEY,
                            title varchar,
                            artist_id varchar NOT NULL REFERENCES artists (artist_id),
                            year int,
                            duration decimal
                            )
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
                                songplay_id int IDENTITY(0,1) PRIMARY KEY,
                                start_time bigint NOT NULL REFERENCES time (start_time),
                                user_id int NOT NULL REFERENCES users (user_id),
                                level varchar,
                                song_id varchar REFERENCES songs (song_id),
                                artist_id varchar REFERENCES artists (artist_id),
                                session_id int,
                                location varchar,
                                user_agent varchar
                                )
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {}
iam_role {}
JSON {}
region '{}'
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'], 'us-west-2')

staging_songs_copy = ("""
COPY staging_songs
FROM {}
iam_role {}
JSON 'auto'
region '{}'
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'], 'us-west-2')

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
