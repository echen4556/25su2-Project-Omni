from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Single blueprint for all player statistics
playerStats = Blueprint('playerStats', __name__)

# --- HELPER FUNCTIONS ---

def get_game_instance_id(cursor, profileID, gameID):
    """Retrieve the gameInstanceID."""
    cursor.execute(
        'SELECT gameInstanceID FROM gamesProfiles WHERE profileID = %s AND gameID = %s',
        (profileID, gameID)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def get_stat_table_id(cursor, profileID, gameID):
    """Retrieve the statTableID for a player in a game."""
    game_instance_id = get_game_instance_id(cursor, profileID, gameID)
    if not game_instance_id:
        return None
    cursor.execute(
        'SELECT statTableID FROM playerStats WHERE gameInstanceID = %s',
        (game_instance_id,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

# --- 1. PLAYER SUMMARY STATS ---

@playerStats.route('/summary/<int:profileID>/<int:gameID>', methods=['GET'])
def get_player_summary_stats(profileID, gameID):
    cursor = db.get_db().cursor()
    cursor.execute('''
        SELECT ps.* FROM playerStats ps
        JOIN gamesProfiles gp ON ps.gameInstanceID = gp.gameInstanceID
        WHERE gp.profileID = %s AND gp.gameID = %s
    ''', (profileID, gameID))
    data = cursor.fetchone()
    if not data:
        return make_response(jsonify({'error': 'Stats not found'}), 404)
    return jsonify(data)

@playerStats.route('/summary/<int:profileID>/<int:gameID>', methods=['POST'])
def create_player_summary_stats(profileID, gameID):
    cursor = db.get_db().cursor()
    game_instance_id = get_game_instance_id(cursor, profileID, gameID)
    if not game_instance_id:
        return make_response(jsonify({'error': 'Player not found for this game'}), 404)

    stats_info = request.json
    query = '''
        INSERT INTO playerStats (gameInstanceID, kills, deaths, assists, totalDamage, totalHeadshots, totalShotsHit, totalWins)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (
        game_instance_id,
        stats_info.get('kills', 0),
        stats_info.get('deaths', 0),
        stats_info.get('assists', 0),
        stats_info.get('totalDamage', 0),
        stats_info.get('totalHeadshots', 0),
        stats_info.get('totalShotsHit', 0),
        stats_info.get('totalWins', 0)
    )
    cursor.execute(query, params)
    db.get_db().commit()
    return make_response(jsonify({'message': 'Player summary stats created'}), 201)

@playerStats.route('/summary/<int:profileID>/<int:gameID>', methods=['PUT'])
def update_player_summary_stats(profileID, gameID):
    cursor = db.get_db().cursor()
    game_instance_id = get_game_instance_id(cursor, profileID, gameID)
    if not game_instance_id:
        return make_response(jsonify({'error': 'Player not found for this game'}), 404)

    stats_info = request.json
    update_fields = [f"{key} = %s" for key in stats_info if key in [
        'kills', 'deaths', 'assists', 'totalDamage', 'totalHeadshots', 'totalShotsHit', 'totalWins']]
    if not update_fields:
        return make_response(jsonify({'error': 'No valid fields for update'}), 400)

    params = [stats_info[key] for key in stats_info if key in [
        'kills', 'deaths', 'assists', 'totalDamage', 'totalHeadshots', 'totalShotsHit', 'totalWins']]
    params.append(game_instance_id)
    query = f'UPDATE playerStats SET {", ".join(update_fields)} WHERE gameInstanceID = %s'
    cursor.execute(query, tuple(params))
    db.get_db().commit()
    return jsonify({'message': 'Player summary stats updated'})

@playerStats.route('/summary/<int:profileID>/<int:gameID>', methods=['DELETE'])
def delete_player_summary_stats(profileID, gameID):
    cursor = db.get_db().cursor()
    game_instance_id = get_game_instance_id(cursor, profileID, gameID)
    if not game_instance_id:
        return make_response(jsonify({'error': 'Player not found for this game'}), 404)

    cursor.execute('DELETE FROM playerStats WHERE gameInstanceID = %s', (game_instance_id,))
    db.get_db().commit()
    return jsonify({'message': 'Player summary stats deleted'})

# --- 2. WEAPON STATS ENDPOINTS ---

@playerStats.route('/playerstats/weapon/<int:profileID>/<int:gameID>/<int:weaponID>', methods=['GET'])
def get_player_weapon_stats(profileID, gameID, weaponID):
    """GET stats for a specific weapon for a player in a game."""
    current_app.logger.info(f'GET /playerstats/weapon/{profileID}/{gameID}/{weaponID}')
    cursor = db.get_db().cursor()
    query = '''
        SELECT ws.* FROM weaponStats ws
        JOIN playerStats ps ON ws.statTableID = ps.statTableID
        JOIN gamesProfiles gp ON ps.gameInstanceID = gp.gameInstanceID
        WHERE gp.profileID = %s AND gp.gameID = %s AND ws.weaponID = %s
    '''
    cursor.execute(query, (profileID, gameID, weaponID))
    data = cursor.fetchone()
    if not data:
        return make_response(jsonify({'error': 'Weapon stats not found'}), 404)
    return make_response(jsonify(data), 200)

@playerStats.route('/weapon/<int:profileID>/<int:gameID>', methods=['GET'])
def get_all_player_weapon_stats(profileID, gameID):
    """GET all weapon stats for a player in a game, including weapon names."""
    current_app.logger.info(f'GET /playerstats/weapon/{profileID}/{gameID}')
    cursor = db.get_db().cursor()
    # JOIN with the weapons table to get the name
    query = '''
        SELECT ws.*, w.name FROM weaponStats ws
        JOIN weapons w ON ws.weaponID = w.weaponID
        JOIN playerStats ps ON ws.statTableID = ps.statTableID
        JOIN gamesProfiles gp ON ps.gameInstanceID = gp.gameInstanceID
        WHERE gp.profileID = %s AND gp.gameID = %s
    '''
    cursor.execute(query, (profileID, gameID))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

@playerStats.route('/weapon/<int:profileID>/<int:gameID>', methods=['POST'])
def create_player_weapon_stats(profileID, gameID):
    """POST new weapon stats for a player in a game."""
    current_app.logger.info(f'POST /playerstats/weapon/{profileID}/{gameID}')
    cursor = db.get_db().cursor()
    stat_table_id = get_stat_table_id(cursor, profileID, gameID)
    if not stat_table_id:
        return make_response(jsonify({'error': 'Player summary stats do not exist for this game'}), 404)

    stats_info = request.json
    query = '''
        INSERT INTO weaponStats (statTableID, weaponID, totalUsageTime, kills, accuracy, amountBought)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    params = (
        stat_table_id, stats_info['weaponID'], stats_info.get('totalUsageTime', 0),
        stats_info.get('kills', 0), stats_info.get('accuracy'), stats_info.get('amountBought', 0)
    )
    cursor.execute(query, params)
    db.get_db().commit()
    return make_response(jsonify({'message': 'Weapon stats created'}), 201)

@playerStats.route('/weapon/<int:profileID>/<int:gameID>/<int:weaponID>', methods=['PUT'])
def update_player_weapon_stats(profileID, gameID, weaponID):
    """PUT (update) weapon stats for a player."""
    current_app.logger.info(f'PUT /playerstats/weapon/{profileID}/{gameID}/{weaponID}')
    cursor = db.get_db().cursor()
    stat_table_id = get_stat_table_id(cursor, profileID, gameID)
    if not stat_table_id:
        return make_response(jsonify({'error': 'Player summary stats not found'}), 404)

    stats_info = request.json
    update_fields = [f"{key} = %s" for key in stats_info if key in ['totalUsageTime', 'kills', 'accuracy', 'amountBought']]
    if not update_fields:
        return make_response(jsonify({'error': 'No valid fields for update'}), 400)

    params = list(stats_info.values())
    params.extend([stat_table_id, weaponID])
    query = f'UPDATE weaponStats SET {", ".join(update_fields)} WHERE statTableID = %s AND weaponID = %s'
    cursor.execute(query, tuple(params))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Weapon stats updated'}), 200)

@playerStats.route('/weapon/<int:profileID>/<int:gameID>/<int:weaponID>', methods=['DELETE'])
def delete_player_weapon_stats(profileID, gameID, weaponID):
    """DELETE weapon stats for a player."""
    current_app.logger.info(f'DELETE /playerstats/weapon/{profileID}/{gameID}/{weaponID}')
    cursor = db.get_db().cursor()
    stat_table_id = get_stat_table_id(cursor, profileID, gameID)
    if not stat_table_id:
        return make_response(jsonify({'error': 'Player summary stats not found'}), 404)

    cursor.execute('DELETE FROM weaponStats WHERE statTableID = %s AND weaponID = %s', (stat_table_id, weaponID))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Weapon stats deleted'}), 200)


# --- 3. MAP STATS ENDPOINTS ---

@playerStats.route('/map/<int:profileID>/<int:gameID>/<int:mapID>', methods=['GET'])
def get_player_map_stats(profileID, gameID, mapID):
    """GET stats for a specific map for a player in a game."""
    current_app.logger.info(f'GET /playerstats/map/{profileID}/{gameID}/{mapID}')
    cursor = db.get_db().cursor()
    query = '''
        SELECT ms.* FROM mapStats ms
        JOIN playerStats ps ON ms.statTableID = ps.statTableID
        JOIN gamesProfiles gp ON ps.gameInstanceID = gp.gameInstanceID
        WHERE gp.profileID = %s AND gp.gameID = %s AND ms.mapID = %s
    '''
    cursor.execute(query, (profileID, gameID, mapID))
    data = cursor.fetchone()
    if not data:
        return make_response(jsonify({'error': 'Map stats not found'}), 404)
    return make_response(jsonify(data), 200)

@playerStats.route('/map/<int:profileID>/<int:gameID>', methods=['GET'])
def get_all_player_map_stats(profileID, gameID):
    """GET all map stats for a player in a game, including map names."""
    current_app.logger.info(f'GET /playerstats/map/{profileID}/{gameID}')
    cursor = db.get_db().cursor()
    # JOIN with the map table to get the name
    query = '''
        SELECT ms.*, m.Name as name FROM mapStats ms
        JOIN map m ON ms.mapID = m.mapID
        JOIN playerStats ps ON ms.statTableID = ps.statTableID
        JOIN gamesProfiles gp ON ps.gameInstanceID = gp.gameInstanceID
        WHERE gp.profileID = %s AND gp.gameID = %s
    '''
    cursor.execute(query, (profileID, gameID))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

@playerStats.route('/map/<int:profileID>/<int:gameID>', methods=['POST'])
def create_player_map_stats(profileID, gameID):
    """POST new map stats for a player in a game."""
    current_app.logger.info(f'POST /playerstats/map/{profileID}/{gameID}')
    cursor = db.get_db().cursor()
    stat_table_id = get_stat_table_id(cursor, profileID, gameID)
    if not stat_table_id:
        return make_response(jsonify({'error': 'Player summary stats do not exist for this game'}), 404)

    stats_info = request.json
    query = '''
        INSERT INTO mapStats (statTableID, mapID, kills, wins, losses)
        VALUES (%s, %s, %s, %s, %s)
    '''
    params = (
        stat_table_id, stats_info['mapID'], stats_info.get('kills', 0),
        stats_info.get('wins', 0), stats_info.get('losses', 0)
    )
    cursor.execute(query, params)
    db.get_db().commit()
    return make_response(jsonify({'message': 'Map stats created'}), 201)

@playerStats.route('/map/<int:profileID>/<int:gameID>/<int:mapID>', methods=['PUT'])
def update_player_map_stats(profileID, gameID, mapID):
    """PUT (update) map stats for a player."""
    current_app.logger.info(f'PUT /playerstats/map/{profileID}/{gameID}/{mapID}')
    cursor = db.get_db().cursor()
    stat_table_id = get_stat_table_id(cursor, profileID, gameID)
    if not stat_table_id:
        return make_response(jsonify({'error': 'Player summary stats not found'}), 404)

    stats_info = request.json
    update_fields = [f"{key} = %s" for key in stats_info if key in ['kills', 'wins', 'losses']]
    if not update_fields:
        return make_response(jsonify({'error': 'No valid fields for update'}), 400)

    params = list(stats_info.values())
    params.extend([stat_table_id, mapID])
    query = f'UPDATE mapStats SET {", ".join(update_fields)} WHERE statTableID = %s AND mapID = %s'
    cursor.execute(query, tuple(params))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Map stats updated'}), 200)

@playerStats.route('/map/<int:profileID>/<int:gameID>/<int:mapID>', methods=['DELETE'])
def delete_player_map_stats(profileID, gameID, mapID):
    """DELETE map stats for a player."""
    current_app.logger.info(f'DELETE /playerstats/map/{profileID}/{gameID}/{mapID}')
    cursor = db.get_db().cursor()
    stat_table_id = get_stat_table_id(cursor, profileID, gameID)
    if not stat_table_id:
        return make_response(jsonify({'error': 'Player summary stats not found'}), 404)

    cursor.execute('DELETE FROM mapStats WHERE statTableID = %s AND mapID = %s', (stat_table_id, mapID))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Map stats deleted'}), 200)
