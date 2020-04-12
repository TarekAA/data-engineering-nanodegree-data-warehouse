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

songplay_table_insert = ("""INSERT INTO songplays 
(start_time, user_id, level, song_id, 
artist_id, session_id,
location, user_agent) 
(
SELECT se.ts, se.userId, se.level, ss.song_id, ss.artist_id, se.sessionId, se.location, se.userAgent 
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title
)
""")

user_table_insert = ("""INSERT INTO users 
(user_id, first_name, last_name, gender, level) 
(
SELECT distinct se.userId, se.firstName, se.lastName, se.gender, se.level
FROM staging_events se
WHERE se.userId IS NOT NULL
ORDER BY se.ts desc
)
""")

song_table_insert = ("""INSERT INTO songs 
(song_id, title, artist_id, year, duration) 
(
SELECT distinct ss.song_id, ss.title, ss.artist_id, ss.year, ss.duration
FROM staging_songs ss
WHERE song_id IS NOT NULL
) 
""")

artist_table_insert = ("""INSERT INTO artists 
(artist_id, name, location, latitude, longitude) 
(
SELECT distinct ss.artist_id, ss.artist_name, ss.artist_location, ss.artist_latitude, ss.artist_longitude
FROM staging_songs ss
WHERE artist_id IS NOT NULL
)
""")

time_table_insert = ("""INSERT INTO time 
(start_time, hour, day, week, month, year, weekday) 
(
SELECT se_ts_cnv.ts, EXTRACT(hour from se_ts_cnv.ts_cnv), EXTRACT(day from se_ts_cnv.ts_cnv), EXTRACT(week from se_ts_cnv.ts_cnv), EXTRACT(month from se_ts_cnv.ts_cnv), EXTRACT(year from se_ts_cnv.ts_cnv), EXTRACT(weekday from se_ts_cnv.ts_cnv)
FROM (
    SELECT ts, TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS ts_cnv FROM staging_events
    WHERE staging_events.ts IS NOT NULL) se_ts_cnv
)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, artist_table_create,
                        song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert,
                        time_table_insert]
