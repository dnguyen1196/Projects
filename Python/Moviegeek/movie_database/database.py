import MySQLdb
import re
import numpy

MOVIE_INSERT_QUERY = '''INSERT INTO Movies (
    movie_id, name, year, C_action, C_adventure, C_animation, C_children, C_comedy,
    C_crime, C_documentary, C_drama, C_fantasy, C_film_noir, C_horror, C_musical,
    C_mystery, C_romance, C_sci_fi, C_thriller, C_war, C_western, rating
)
VALUES
'''

MOVIE_COUNT = 3952

USER_INSERT_QUERY = '''INSERT INTO Users VALUES'''

RATING_INSERT_QUERY = '''INSERT INTO Ratings VALUES'''

MOVIE_RATING_UPDATE_QUERY = '''UPDATE Movies SET rating = {} WHERE movie_id = {}'''

CATEGORY = {"Action":0, 
            "Adventure":1,
            "Animation":2,
            "Children's":3,
            "Comedy":4,
            "Crime":5,
            "Documentary":6,
            "Drama":7,
            "Fantasy":8,
            "Film-Noir":9,
            "Horror":10,
            "Musical":11,
            "Mystery":12,
            "Romance":13,
            "Sci-Fi":14,
            "Thriller":15,
            "War":16,
            "Western":17
        }

def database_connect():
    try:
        db = MySQLdb.connect("localhost","movie_lens","euclid96","MovieLens")
    except mysql.connector.Error as err:
        print ("Cannot connect to the database {}".format(err))
    # prepare a cursor object using cursor() method
    return db

def ratings_data_parse(line):
    (user_id, movie_id, rating, time) = line.split("::")
    return (user_id, movie_id, rating, time)

def user_data_parse(line):
    (user_id, gender, age, occupation, zip) = line.split("::")
    return (user_id, gender, age, occupation, zip)


def parse_category(category):
    genre = numpy.zeros(18, dtype=int)
    for i in range(len(category)):
        index = CATEGORY[category[i]]
        genre[index] = 1
    return genre


def movie_data_parse(line):
    (movie_id, name, genre) = line.split("::")
    try:
        (title, unformatted_year) = name.split("(")
        year = unformatted_year.split(")")[0]
    except ValueError: 
    # The case where there is a parenthesis in the movie name
        try:
            (title, alias, unformatted_year) = name.split("(")
            title = title + "(" + alias
            year = unformatted_year.split(")")[0]
        except ValueError:
            (title, alias1, alias2, unformatted_year) = name.split("(")
            title = title + "(" + alias1 + " (" + alias2
            year = unformatted_year.split(")")[0]

    category = genre.split("|")
    types = parse_category(category)
    return (movie_id, title, year, types)

def movie_table_query_create(movie_id, title, year, types):
    query = '({},"{}",{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'
    query = query.format(movie_id, title, year, *types)
    query = query + "NULL);"
    query = MOVIE_INSERT_QUERY + query
    return query

def movie_table_insert(database):
    f = open('movies.dat', 'r')
    cursor = database.cursor()
    # Loop through the entire movie data sets
    for line in f:
        line = line.rstrip('\n')
        (movie_id, title, year, types) = movie_data_parse(line)
        query = movie_table_query_create(movie_id, title, year, types)
        try:
            cursor.execute(query)
        except:
            database.rollback()
    
    database.commit()
    f.close()

def user_table_query_create(user_id, gender, age, occupation, zip):
    query = "{}, '{}', {}, {}, '{}'"
    query = query.format(user_id, gender, age, occupation, zip)
    query = USER_INSERT_QUERY + " (" + query + ");"
    return query

def user_table_insert(database):
    f = open('users.dat', 'r')
    cursor = database.cursor()
    # Loop through the entire user data sets
    for line in f:
        line = line.rstrip('\n')
        (user_id, gender, age, occupation, zip) = user_data_parse(line)
        query = user_table_query_create(user_id, gender, age, occupation, zip)
        try:
            cursor.execute(query)
        except:
            database.rollback()
    database.commit()
    f.close()

def rating_table_query_create(user_id, movie_id, rating, time):
    query = "({}, {}, {}, '{}');"
    query = query.format(user_id, movie_id, rating, time)
    query = RATING_INSERT_QUERY + query
    return query

def rating_table_insert(database):
    f = open('ratings.dat', 'r')
    cursor = database.cursor()

    rating_count = numpy.zeros(MOVIE_COUNT+1, dtype=int) # Number of votes
    total_score = numpy.zeros(MOVIE_COUNT+1, dtype=int) # Total score
    
    # Loop through the entire ratings data set
    for line in f:
        line = line.rstrip('\n')
        (user_id, movie_id, rating, time) = ratings_data_parse(line)

        rating_count[int(movie_id)] += 1
        total_score[int(movie_id)] += int(rating)

        query = rating_table_query_create(user_id, movie_id, rating, time)
        try:
            cursor.execute(query)
        except:
            database.rollback()

    database.commit()
    f.close()

    # Write rating data to a file
    f = open('movie_score.dat', 'w')
    for i in range(1, MOVIE_COUNT+1):
        line = str(rating_count[i]) + " " + str(total_score[i])
        f.write(line)
        f.write('\n')

def movie_rating_update(database):
    f = open('movie_score.dat', 'r')
    cursor = database.cursor()
    movie_id = 1

    for line in f:
        line = line.rstrip("\n")
        (count, score) = line.split(" ")
        try:
            rating = float(score)/float(count)
        except ZeroDivisionError:
            rating = 'NULL'
        query = MOVIE_RATING_UPDATE_QUERY.format(rating, movie_id)
        movie_id += 1
        try:
            cursor.execute(query)
        except:
            database.rollback()
    
    database.commit()
    f.close()


def main():
    # Connect to database
    database = database_connect()

    # INSERT MOVIE DATA INTO TABLE
    # movie_table_insert(database)

    # INSERT USER DATA INTO TABLE
    # user_table_insert(database)
    
    # INSERT USER
    # rating_table_insert(database)

    movie_rating_update(database)


main()



