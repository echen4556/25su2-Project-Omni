from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

games = Blueprint('games', __name__)

# GET all games
@games.route('/', methods=['GET'])
def get_games():
    current_app.logger.info('GET /games')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM games ORDER BY gameID')
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET one game
@games.route('/<gameID>', methods=['GET'])
def get_game(gameID):
    current_app.logger.info(f'GET /game/{gameID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM games WHERE gameID = %s', (gameID,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a game
@games.route('/', methods=['POST'])
def create_game():
    current_app.logger.info('POST /games')
    info = request.json
    name = info.get('name')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO games (name) VALUES (%s)', (name,))
    db.get_db().commit()
    return 'Game created!', 201

# PUT update a game
@games.route('/<gameID>', methods=['PUT'])
def update_game(gameID):
    current_app.logger.info(f'PUT /game/{gameID}')
    info = request.json
    name = info.get('name')
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE games SET name = %s WHERE gameID = %s', (name, gameID))
    db.get_db().commit()
    return 'Game updated!', 200

# DELETE a game
@games.route('/<gameID>', methods=['DELETE'])
def delete_game(gameID):
    current_app.logger.info(f'DELETE /game/{gameID}')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM games WHERE gameID = %s', (gameID,))
    db.get_db().commit()
    return 'Game deleted!', 200
