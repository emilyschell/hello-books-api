from app import db
from app.models.book import Book
from app.models.genre import Genre
from flask import Blueprint, jsonify, make_response, request, abort

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")


def validate_genre(genre_id):
    try:
        genre_id = int(genre_id)
    except:
        abort(make_response({"message": f"genre {genre_id} invalid"}, 400))
    genre = Genre.query.get(genre_id)
    if not genre:
        abort(make_response({"message": f"genre {genre_id} not found"}, 404))
    return genre

# ROUTES


@genres_bp.route("/<genre_id>/books", methods=["GET"])
def get_books_by_genre(genre_id):
    genre = validate_genre(genre_id)
    books_response = [book.to_dict() for book in genre.books]
    return jsonify(books_response), 200


@genres_bp.route("", methods=["GET"])
def read_all_genres():
    genres_response = []
    name_query = request.args.get("name")
    if name_query:
        genres = Genre.query.filter_by(name=name_query)
    else:
        genres = Genre.query.all()
    for genre in genres:
        genres_response.append({
            "id": genre.id,
            "name": genre.name
        })
    return jsonify(genres_response), 200


@genres_bp.route("/<genre_id>", methods=["GET"])
def read_one_genre(genre_id):
    genre = validate_genre(genre_id)
    return {
        "id": genre.id,
        "name": genre.name
    }


@genres_bp.route("", methods=["POST"])
def add_genre():
    request_body = request.get_json()
    if "name" not in request_body:
        return make_response("Invalid Request", 400)
    new_genre = Genre(name=request_body["name"])

    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(f"Genre {new_genre.name} successfully created"), 201)


@genres_bp.route("/<genre_id>/books", methods=["POST"])
def create_book(genre_id):
    genre = validate_genre(genre_id)
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)
    new_book = Book(title=request_body["title"],
                    description=request_body["description"],
                    author_id=request_body["author_id"],
                    genres=[genre])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"{new_book.genres[0].name} book {new_book.title} by {new_book.author.name} successfully created"), 201)
