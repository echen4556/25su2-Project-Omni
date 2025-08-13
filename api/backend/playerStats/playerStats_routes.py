from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

playerStats = Blueprint('playerStats', __name__)

# GET stats for a WEAPON used by a specific player in a specific game
@playerStats.route('/playerStats/<profileID>/<gameID>/<weaponID>', methods=['GET'])
def get_player_weapon_stats(profileID, gameID, weaponID):
    current_app.logger.info(f'GET /playerStats/{profileID}/{gameID}/{weaponID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM weaponStats 
                      WHERE profileID = %s AND gameID = %s AND weaponID = %s''',
                   (profileID, gameID, weaponID))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# GET stats for a MAP by a specific player in a specific game
@playerStats.route('/playerStats/<profileID>/<gameID>/<mapID>', methods=['GET'])
def get_player_map_stats(profileID, gameID, mapID):
    current_app.logger.info(f'GET /playerStats/{profileID}/{gameID}/{mapID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM mapStats
                      WHERE profileID = %s AND gameID = %s AND mapID = %s''',
                   (profileID, gameID, mapID))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST create stats entry
@playerStats.route('/playerStats/<profileID>/<gameID>/<weaponID>', methods=['POST'])
def create_player_weapon_stats(profileID, gameID, weaponID):
    current_app.logger.info(f'POST /playerStats/{profileID}/{gameID}/{weaponID}')
    stats_info = request.json
    kills = stats_info.get('kills', 0)
    deaths = stats_info.get('deaths', 0)
    accuracy = stats_info.get('accuracy', None)
    query = '''INSERT INTO weaponStats (profileID, gameID, weaponID, kills, deaths, accuracy)
               VALUES (%s, %s, %s, %s, %s, %s)'''
    cursor = db.get_db().cursor()
    cursor.execute(query, (profileID, gameID, weaponID, kills, deaths, accuracy))
    db.get_db().commit()
    return 'Player weapon stats created!', 201

# PUT update stats
@playerStats.route('/playerStats/<profileID>/<gameID>/<weaponID>', methods=['PUT'])
def update_player_weapon_stats(profileID, gameID, weaponID):
    current_app.logger.info(f'PUT /playerStats/{profileID}/{gameID}/{weaponID}')
    stats_info = request.json
    kills = stats_info.get('kills')
    deaths = stats_info.get('deaths')
    accuracy = stats_info.get('accuracy')
    query = '''UPDATE weaponStats 
               SET kills = %s, deaths = %s, accuracy = %s
               WHERE profileID = %s AND gameID = %s AND weaponID = %s'''
    cursor = db.get_db().cursor()
    cursor.execute(query, (kills, deaths, accuracy, profileID, gameID, weaponID))
    db.get_db().commit()
    return 'Player weapon stats updated!', 200

# DELETE stats record
@playerStats.route('/playerStats/<profileID>/<gameID>/<weaponID>', methods=['DELETE'])
def delete_player_weapon_stats(profileID, gameID, weaponID):
    current_app.logger.info(f'DELETE /playerStats/{profileID}/{gameID}/{weaponID}')
    cursor = db.get_db().cursor()
    cursor.execute('''DELETE FROM weaponStats
                      WHERE profileID = %s AND gameID = %s AND weaponID = %s''',
                   (profileID, gameID, weaponID))
    db.get_db().commit()
    return 'Player weapon stats deleted!', 200

# GET all weapons stats for a player in a game
@playerStats.route('/playerStats/<profileID>/<gameID>', methods=['GET'])
def get_all_weapon_stats_for_player(profileID, gameID):
    current_app.logger.info(f'GET /playerStats/{profileID}/{gameID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM weaponStats
                      WHERE profileID = %s AND gameID = %s''',
                   (profileID, gameID))
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
