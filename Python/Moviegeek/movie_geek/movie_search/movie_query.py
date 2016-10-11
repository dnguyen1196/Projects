# Need a function that takes in the category string and create
from movie_search.models import *
from django.core import serializers
from django.db.models import Q
import logging

MOVIE_CATEGORIES = ["C_action", "C_adventure", "C_animation", "C_children", "C_comedy", "C_crime", "C_documentary", "C_drama", "C_fantasy", "C_film_noir", "C_horror", "C_musical", "C_mystery", "C_romance", "C_sci_fi", "C_thriller", "C_war", "C_western"]

MOVIE_MYSQL_QUERY = "SELECT movie_id, name, year, rating FROM Movies WHERE ("

MOVIE_QUERY_LIMIT = 15

# Logger for debugging purposes
logger = logging.getLogger(__name__)

# We can guarantee that category is a valid string of 18 characters
def create_movie_query(category):
    filter = ""
    for i in range(len(category)):
        if (category[i] == '1'):
            # If the current filter already has some input
            if (len(filter) > 0):
                filter += " OR "
            filter += MOVIE_CATEGORIES[i] + " = 1"
    
    if (len(filter) > 0):
        filter += " ) AND rating IS NOT NULL AND rating < 5 ORDER BY -rating"  
    else: # If the user gives no indication of movie category
        filter = '''SELECT movie_id, name, year, rating FROM Movies 
        WHERE rating IS NOT NULL  AND rating < 5 ORDER BY -rating'''
        return filter

    query = MOVIE_MYSQL_QUERY + filter
    return query

def perform_movie_query(category):
    # Create an array of query parameters
    query = create_movie_query(category)

    # Perform raw mysql query
    movie = Movies.objects.raw(query)[:MOVIE_QUERY_LIMIT]

    # Serialize the movie list (as JSON string)
    movie_list = serializers.serialize("json", movie)
    return movie_list
