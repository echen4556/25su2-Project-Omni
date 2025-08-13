from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

maps = Blueprint('map', __name__)

# GET all maps for a game
@maps.route('/map/<gameID>', methods=['GET'])
def get_maps_for_game(gameID):
    current_app.logger.info(f'GET /map/{gameID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT map_id, name FROM map WHERE game_id = %s', (gameID,))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET specific map details
@maps.route('/map/<gameID>/<mapID>', methods=['GET'])
def get_map_info(gameID, mapID):
    current_app.logger.info(f'GET /map/{gameID}/{mapID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM map WHERE game_id = %s AND map_id = %s', (gameID, mapID))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create a new map
@maps.route('/map/<gameID>/<mapID>', methods=['POST'])
def create_map(gameID, mapID):
    current_app.logger.info(f'POST /map/{gameID}/{mapID}')
    map_info = request.json
    name = map_info['name']
    info = map_info.get('info', None)
    query = 'INSERT INTO map (map_id, game_id, name, info) VALUES (%s, %s, %s, %s)'
    cursor = db.get_db().cursor()
    cursor.execute(query, (mapID, gameID, name, info))
    db.get_db().commit()
    return 'Map created successfully!', 201

# PUT update a map
@maps.route('/map/<gameID>/<mapID>', methods=['PUT'])
def update_map(gameID, mapID):
    current_app.logger.info(f'PUT /map/{gameID}/{mapID}')
    map_info = request.json
    name = map_info.get('name')
    info = map_info.get('info')
    query = 'UPDATE map SET name = %s, info = %s WHERE game_id = %s AND map_id = %s'
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, info, gameID, mapID))
    db.get_db().commit()
    return 'Map updated successfully!', 200

# DELETE remove a map
@maps.route('/map/<gameID>/<mapID>', methods=['DELETE'])
def delete_map(gameID, mapID):
    current_app.logger.info(f'DELETE /map/{gameID}/{mapID}')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM map WHERE game_id = %s AND map_id = %s', (gameID, mapID))
    db.get_db().commit()
    return 'Map deleted successfully!', 200
