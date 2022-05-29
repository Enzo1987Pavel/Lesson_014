import sqlite3
from collections import Counter


class NetflixDatabase:

    def __init__(self, netflix_path):
        """Указываем путь к базе данных 'netflix.db'
            и создаем подключение к базе данных"""
        self.con = sqlite3.connect(netflix_path)
        self.cur = self.con.cursor()


def search_movie(movie_title):
    """Поиск самого 'свежего' добавленного фильма при совпадении годов выпуска"""
    ndb_con = NetflixDatabase("netflix.db")

    # Выбираем из title, country, release_year, listed_in, description, MAX(date_added) [последний - если совпадают года выпуска фильмов, то выбирается последний]
    sqlite_query = f"""
                    SELECT title, country, MAX(release_year), listed_in, description, MAX(date_added)
                    FROM netflix
                    WHERE title LIKE '%{movie_title}%' COLLATE NOCASE
                    AND type = 'Movie'
                    AND title IS NOT NULL
    """
    ndb_con.cur.execute(sqlite_query)
    result = ndb_con.cur.fetchall()

    # Вывод результатов. Первое значение списка - название столбца, второе - его значение
    result_search_title = {
        "Название": result[0][0],
        "Страна": result[0][1],
        "Год выпуска": result[0][2],
        "Жанр": result[0][3],
        "Описание": result[0][4],
    }
    return result_search_title


def movies_range(min_year, max_year):
    """Функция для фильтрации фильмов по годам от 'min_year' до 'max_year'"""
    ndb_con = NetflixDatabase("netflix.db")

    sqlite_query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN '{min_year}' AND {max_year}
                    AND type = 'Movie'
                    LIMIT 100
    """
    ndb_con.cur.execute(sqlite_query)
    result = ndb_con.cur.fetchall()
    result_list = []  # пустой список для добавления результатов

    for movie in result:
        result_list.append({
            "Название": movie[0],
            "Год выпуска": movie[1],
            })
    return result_list


def movies_by_rating(rating):
    """Функция для фильтрации допустимых рейтингов фильмов"""
    ndb_con = NetflixDatabase("netflix.db")

    # Создаем словарь с допустимыми рейтингами фильмов
    movies_rating = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'",
    }

    sqlite_query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ({movies_rating[rating]})
    """
    ndb_con.cur.execute(sqlite_query)
    result = ndb_con.cur.fetchall()
    movies_rating_list = []
    for movie in result:
        movies_rating_list.append({
            "Название": movie[0],
            "Рейтинг": movie[1],
            "Описание": movie[2],
        })
    return movies_rating_list


def movies_by_genre(genre):
    """Функция для получения 10 самых свежих фильмов по фильтру их жанра в формате JSON-файла"""
    ndb_con = NetflixDatabase("netflix.db")

    sqlite_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    AND type = 'Movie'
                    AND title IS NOT NULL
                    ORDER BY release_year DESC
                    LIMIT 10
    """
    ndb_con.cur.execute(sqlite_query)
    result = ndb_con.cur.fetchall()
    movies_genre_list = []
    for movie in result:
        movies_genre_list.append({
            "Название": movie[0],
            "Описание": movie[1],
        })
    return movies_genre_list


def actors_play(actor_one, actor_two):
    """Функция для получения имен актеров, которые сыграли вместе 2 и более раз"""
    ndb_con = NetflixDatabase("netflix.db")

    sqlite_query = f"""
                    SELECT "cast"
                    FROM netflix
                    WHERE "cast" LIKE '%{actor_one}%'
                    AND "cast" LIKE '%{actor_two}%'
    """
    ndb_con.cur.execute(sqlite_query)
    result = ndb_con.cur.fetchall()
    actors_list = []
    for actor in result:
        actors_list.extend(actor[0].split(", "))  # Добавляем всех актеров, кто играм вместе с нашими указанными

    # Счетчик, который считает все значения в листе, кто из актеров встречался сколько раз
    counter = Counter(actors_list)
    result_cast_list = []
    for cast, count in counter.items():
        if cast not in [actor_one, actor_two] and count > 2:
            result_cast_list.append(cast)
    return result_cast_list


# Для проверки функции 'actors_play'
print(actors_play("Rose McIver", "Ben Lamb"))
print(actors_play("Jack Black", "Dustin Hoffman"))


def movies_parameters(movie_type, movie_year, movie_genre):
    """Функция для выбора типа картины, года её выпуска и жанра в JSON-файле"""
    ndb_con = NetflixDatabase("netflix.db")

    sqlite_query = f"""
                   SELECT type, release_year, listed_in 
                   FROM netflix
                   WHERE type = '{movie_type}'
                   AND release_year = '{movie_year}'
                   AND listed_in LIKE '%{movie_genre}%'
   """
    ndb_con.cur.execute(sqlite_query)
    result = ndb_con.cur.fetchall()
    result_list_of_movies = []

    for movie in result:
        result_list_of_movies.append({
            "Тип картины": movie[0],
            "Год выпуска": movie[1],
            "Жанр": movie[2],
        })

    return result_list_of_movies


# Для проверки функции 'movies_parameters'
print(movies_parameters("Movie", 2006, "Comedy"))
