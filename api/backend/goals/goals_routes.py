from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

goals = Blueprint('goals', __name__)

# GET all goals
@goals.route('/goals/<int:profileID>', methods=['GET'])
def get_goals():
    current_app.logger.info(f'GET /goals/{profileID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM goals ORDER BY goalsID')
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET one goal
@goals.route('/goal/<goalsID>', methods=['GET'])
def get_game(goalsID):
    current_app.logger.info(f'GET /game/{goalsID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM goals WHERE goalsID = %s', (goalsID,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a game
@goals.route('/goals', methods=['POST'])
def create_game():
    current_app.logger.info('POST /goals')
    info = request.json
    name = info.get('name')
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO goals (name) VALUES (%s)', (name,))
    db.get_db().commit()
    return 'Game created!', 201

# PUT update a game
@goals.route('/game/<goalsID>', methods=['PUT'])
def update_game(goalsID):
    current_app.logger.info(f'PUT /game/{goalsID}')
    info = request.json
    name = info.get('name')
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE goals SET name = %s WHERE goalsID = %s', (name, goalsID))
    db.get_db().commit()
    return 'Game updated!', 200

# DELETE a game
@goals.route('/game/<goalsID>', methods=['DELETE'])
def delete_game(goalsID):
    current_app.logger.info(f'DELETE /game/{goalsID}')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM goals WHERE goalsID = %s', (goalsID,))
    db.get_db().commit()
    return 'Game deleted!', 200