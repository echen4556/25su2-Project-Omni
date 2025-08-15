from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

games = Blueprint("games", __name__)

# GET all games  -> final path: /games
@games.route("", methods=["GET"])
@games.route("/", methods=["GET"])
def get_games():
    current_app.logger.info("GET /games")
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM games ORDER BY gameID")
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# GET one game   -> final path: /games/<gameID>
@games.route("/<int:gameID>", methods=["GET"])
def get_game(gameID):
    current_app.logger.info(f"GET /games/{gameID}")
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM games WHERE gameID = %s", (gameID,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

# POST create    -> final path: /games
@games.route("", methods=["POST"])
@games.route("/", methods=["POST"])
def create_game():
    current_app.logger.info("POST /games")
    info = request.get_json(force=True) or {}
    name = info.get("name")
    cursor = db.get_db().cursor()
    cursor.execute("INSERT INTO games (name) VALUES (%s)", (name,))
    db.get_db().commit()
    return "Game created!", 201

# PUT update     -> final path: /games/<gameID>
@games.route("/<int:gameID>", methods=["PUT"])
def update_game(gameID):
    current_app.logger.info(f"PUT /games/{gameID}")
    info = request.get_json(force=True) or {}
    name = info.get("name")
    cursor = db.get_db().cursor()
    cursor.execute("UPDATE games SET name = %s WHERE gameID = %s", (name, gameID))
    db.get_db().commit()
    return "Game updated!", 200

# DELETE         -> final path: /games/<gameID>
@games.route("/<int:gameID>", methods=["DELETE"])
def delete_game(gameID):
    current_app.logger.info(f"DELETE /games/{gameID}")
    cursor = db.get_db().cursor()
    cursor.execute("DELETE FROM games WHERE gameID = %s", (gameID,))
    db.get_db().commit()
    return "Game deleted!", 200
