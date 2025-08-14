from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

profiles = Blueprint('profiles', __name__)

# GET all profiles
@profiles.route('/profiles', methods=['GET'])
def get_profiles():
    current_app.logger.info('GET /profiles')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT profileID, username, isAdmin, isPublic, isPremium FROM profiles ORDER BY profileID')
    data = cursor.fetchall()
    resp = make_response(jsonify(data)); resp.status_code = 200
    return resp

# GET one profile
@profiles.route('/profiles/<profileID>', methods=['GET'])
def get_profile(profileID):
    current_app.logger.info(f'GET /profiles/{profileID}')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT profileID, username, isAdmin, isPublic, isPremium FROM profiles WHERE profileID=%s', (profileID,))
    data = cursor.fetchall()
    if not data:
        return make_response(jsonify({'error':'profile not found'}), 404)
    return make_response(jsonify(data[0]), 200)

# POST create profile
@profiles.route('/profiles', methods=['POST'])
def create_profile():
    current_app.logger.info('POST /profiles')
    info = request.json or {}
    cursor = db.get_db().cursor()
    cursor.execute(
        '''INSERT INTO profiles (username, isAdmin, isPublic, isPremium, password)
           VALUES (%s,%s,%s,%s,%s)''',
        (info.get('username'), info.get('isAdmin', 0), info.get('isPublic', 1), info.get('isPremium', 0), info.get('password', ''))
    )
    db.get_db().commit()
    return 'Profile created!', 201

# PUT update profile
@profiles.route('/profiles/<profileID>', methods=['PUT'])
def update_profile(profileID):
    current_app.logger.info(f'PUT /profiles/{profileID}')
    info = request.json or {}
    cursor = db.get_db().cursor()
    cursor.execute(
        '''UPDATE profiles
           SET username=%s, isAdmin=%s, isPublic=%s, isPremium=%s
           WHERE profileID=%s''',
        (info.get('username'), info.get('isAdmin', 0), info.get('isPublic', 1), info.get('isPremium', 0), profileID)
    )
    db.get_db().commit()
    return 'Profile updated!', 200

# DELETE profile
@profiles.route('/profiles/<profileID>', methods=['DELETE'])
def delete_profile(profileID):
    current_app.logger.info(f'DELETE /profiles/{profileID}')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM profiles WHERE profileID=%s', (profileID,))
    db.get_db().commit()
    return 'Profile deleted!', 200

@profiles.route('/profiles/<profileID>/games', methods=['GET'])
def get_user_games_route(profileID):
    current_app.logger.info(f'GET /profiles/{profileID}/games')
    cursor = db.get_db().cursor()
    cursor.execute(
        'SELECT t2.gameID, t2.name FROM gamesProfiles t1 JOIN games t2 ON t1.gameID = t2.gameID WHERE t1.profileID = %s',
        (profileID,)
    )
    games = cursor.fetchall()
    return jsonify(games), 200

