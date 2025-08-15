# backend/rest_entry/game_profiles.py
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

game_profiles_bp = Blueprint('game_profiles', __name__)

# GET all game-profile links
@game_profiles_bp.route('/gameProfiles', methods=['GET'])
def get_all_game_profiles():
    current_app.logger.info('GET /gameProfiles')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM gamesProfiles')
    data = cursor.fetchall()
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

# POST add a new game-profile link
@game_profiles_bp.route('/gameProfiles', methods=['POST'])
def add_game_profile():
    current_app.logger.info('POST /gameProfiles')
    info = request.json
    gameID = info.get('gameID')
    profileID = info.get('profileID')
    gameUsername = info.get('gameUsername')
    showOnDashboard = info.get('showOnDashboard', True)
    cursor = db.get_db().cursor()
    cursor.execute('''
        INSERT INTO gamesProfiles (gameID, profileID, gameUsername, showOnDashboard)
        VALUES (%s, %s, %s, %s)
    ''', (gameID, profileID, gameUsername, showOnDashboard))
    db.get_db().commit()
    return jsonify({"message": "Game profile link created!"}), 201

# GET details for a specific game-profile link
@game_profiles_bp.route('/gameProfiles/<int:gameInstanceID>', methods=['GET'])
def get_game_profile(gameInstanceID):
    current_app.logger.info(f'GET /gameProfiles/{gameInstanceID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM gamesProfiles WHERE gameInstanceID = %s', (gameInstanceID,))
    data = cursor.fetchone()
    if not data:
        return jsonify({"message": "Game profile not found"}), 404
    return make_response(jsonify(data), 200)

# PUT update a game-profile link
@game_profiles_bp.route('/gameProfiles/<int:gameInstanceID>', methods=['PUT'])
def update_game_profile(gameInstanceID):
    current_app.logger.info(f'PUT /gameProfiles/{gameInstanceID}')
    info = request.json
    gameUsername = info.get('gameUsername')
    showOnDashboard = info.get('showOnDashboard')
    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE gamesProfiles
        SET gameUsername = %s, showOnDashboard = %s
        WHERE gameInstanceID = %s
    ''', (gameUsername, showOnDashboard, gameInstanceID))
    db.get_db().commit()

    return jsonify({"message": "Game profile updated!"}), 200

# "Soft-delete" a game-profile link by hiding it on the dashboard
@game_profiles_bp.route('/gameProfiles/<int:gameInstanceID>', methods=['DELETE'])
def hide_game_profile(gameInstanceID):
    current_app.logger.info(f'SOFT DELETE /gameProfiles/{gameInstanceID}')
    cursor = db.get_db().cursor()
    cursor.execute('''
        UPDATE gamesProfiles
        SET showOnDashboard = FALSE
        WHERE gameInstanceID = %s
    ''', (gameInstanceID,))
    db.get_db().commit()
    return jsonify({"message": "Game profile hidden from dashboard!"}), 200

# GET all games linked to a specific profile
@game_profiles_bp.route('/games/profile/<int:profileID>', methods=['GET'])
def get_games_for_profile(profileID):
    current_app.logger.info(f'GET /games/profile/{profileID}')
    cursor = db.get_db().cursor()
    # Join with the games table to get the game names directly
    query = '''
        SELECT g.gameID, g.name
        FROM games g
        JOIN gamesProfiles gp ON g.gameID = gp.gameID
        WHERE gp.profileID = %s
    '''
    cursor.execute(query, (profileID,))
    data = cursor.fetchall()
    return make_response(jsonify(data), 200)

