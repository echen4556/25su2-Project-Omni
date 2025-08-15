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
