from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

books_bp = Blueprint("books", __name__, url_prefix="/books")

# HELPER FUNCTIONS


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} invalid"}, 400))
    book = Book.query.get(book_id)
    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))
    return book

# ROUTE FUNCTIONS


@books_bp.route("", methods=["GET"])
def read_all_books():
    books_response = []
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }


@books_bp.route("", methods=["POST"])
def add_book():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(f"Book #{book_id} successfully updated")


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()

    return make_response(f"Book #{book_id} successfully deleted, so gone, kthxbaaai.")


# *******OUTDATED CODE*******
# hello_world_bp = Blueprint("hello_world_bp", __name__)


# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     return "Hello, World!"


# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }


# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body


# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description


# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]

# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append(
#             {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }
#         )
#     return jsonify(books_response)
