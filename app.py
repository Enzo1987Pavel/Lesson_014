from json import JSONDecodeError
from types import NoneType

from flask import Flask, render_template, jsonify

from main import *

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/movie/<title>/")
def page_search_movie_title(title):
    try:
        return search_movie(title)
    except (JSONDecodeError, FileNotFoundError) as error_text:
        title_error = "Ошибка загрузки!"
        return render_template("error_template.html", title_error=title_error, error_text=error_text)
    except TypeError as error_text:
        title_error = "Данные не найдены!"
        return render_template("error_template.html", title_error=title_error, error_text=error_text)
    except NoneType as error_text:
        title_error = "Данные не найдены!"
        return render_template("error_template.html", title_error=title_error, error_text=error_text)


@app.route("/movie/<int:min_year>/to/<int:max_year>/")
def page_movies_range(min_year, max_year):
    try:
        return jsonify(movies_range(min_year, max_year))
    except BaseException as error_text:
        title_error = "Ошибка загрузки!"
        return render_template("error_template.html", title_error=title_error, error_text=error_text)


@app.route("/rating/<category>/")
def page_by_rating(category):
    if category not in ["children", "family", "adult"]:
        return "<h2>Указанной группы не существует!</h2><br />" \
               "<p>Для продолжения перейдите на  <a href='/' title='нажмите, чтобы перейти'> главную</a> страницу сайта</p>"
    else:
        return jsonify(movies_by_rating(category))


@app.route("/genre/<genre>/")
def page_movies_by_genre(genre):
    return jsonify(movies_by_genre(genre))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_400.html", e=e), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("error_500.html", e=e), 500


if __name__ == "__main__":
    app.run()
