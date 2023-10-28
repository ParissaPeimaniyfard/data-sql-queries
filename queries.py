# pylint: disable=C0103, missing-docstring
import sqlite3

conn = sqlite3.connect('data/movies.sqlite')
db = conn.cursor()


def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """
    SELECT title, genres, directors.name  from movies
    join directors on movies.director_id = directors.id
    """
    db.execute(query)
    results = db.fetchall()
    return results


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """
    SELECT title from movies
    join directors on movies.director_id = directors.id
    WHERE movies.start_year > directors.death_year
    """
    db.execute(query)
    results = db.fetchall()
    return [results[0][0] for row in results]


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = """
    SELECT COUNT(id), AVG(minutes) from movies
    WHERE genres LIKE 'genre_name'
    """
    db.execute(query)
    results = db.fetchall()
    final= {"genre": genre_name, "number_of_movie": results[0][0], "avg_length": results[0][1]}
    #print(final)
    return final


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = """
    SELECT directors.name, COUNT(*) as count_movies
    from movies
    join directors on movies.director_id = directors.id
    WHERE genres = "Action,Adventure,Comedy"
    GROUP by directors.name
    ORDER BY count_movies DESC, directors.name
    LIMIT 5
    """
    db.execute(query)
    results = db.fetchall()
    return results



def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    '''return the top 5 youngest directors when they direct their first movie'''
    buckets= range(0,991,30)
    list =[]
    for n in buckets:
        query = f"""
        SELECT {n}+30 as max_duration, COUNT(*)
        from movies
        WHERE movies.minutes < {n} + 30 AND movies.minutes >= {n}
        """
        db.execute(query)
        results = db.fetchall()
        if results[0][1] != 0:
            list.append(results)
    return list


def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """
    SELECT directors.name, movies.start_year - directors.birth_year as age_directors
    FROM movies
    join directors on movies.director_id = directors.id
    WHERE directors.birth_year IS NOT NULL
    ORDER BY age_directors
    LIMIT 5
    """
    db.execute(query)
    results = db.fetchall()
    return results
#print(movie_duration_buckets(db))
#print (top_five_directors_for (db, "action"))
